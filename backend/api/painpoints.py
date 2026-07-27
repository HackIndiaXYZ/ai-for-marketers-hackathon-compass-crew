import json
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
import anthropic
from database.mongodb import get_database, serialize_doc
from database.schemas import PainPointResponse, PainPointListResponse
from api.auth import get_current_user

router = APIRouter(prefix="/api/painpoints", tags=["painpoints"])


async def _generate_insight_narrative(pain_points: list, topic: str) -> str:
    try:
        client = anthropic.Anthropic()

        pain_summary = json.dumps(
            [{"text": p["text"], "frequency": p["frequency"], "emotion_type": p["emotion_type"],
              "emotion_score": p["emotion_score"], "rank": p["rank"]} for p in pain_points],
            indent=2,
        )

        prompt = f"""You are a senior marketing strategist writing a brief for a small business owner.

Topic: {topic}
Pain points discovered (ranked by frequency):
{pain_summary}

Write a 3-4 sentence plain English narrative that explains:
1. Which pain point matters most and why
2. Which type of customer to target first
3. What ad angle would work best

Write like you're talking to a smart friend who runs a small business. No jargon. No bullet points. Max 4 sentences."""

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )

        narrative = ""
        for block in response.content:
            if block.type == "text":
                narrative += block.text
        return narrative.strip()

    except Exception:
        return f"The most significant pain point for {topic} relates to customer frustration. Target users experiencing this emotion first, as they have the highest intent to switch. Use emotional, solution-focused ad copy that validates their frustration and offers immediate relief."


@router.post("/extract", response_model=PainPointListResponse)
async def extract_painpoints(
    analysis_id: str,
    raw_text: str,
    current_user: dict = Depends(get_current_user),
):
    try:
        db = get_database()

        analysis = await db.analyses.find_one({"_id": analysis_id, "user_id": current_user["id"]})
        if not analysis:
            raise HTTPException(status_code=404, detail={"error": "Not found", "detail": "Analysis not found"})

        client = anthropic.Anthropic()

        prompt = f"""You are a marketing intelligence analyst.

From these real customer complaints, extract 5-8 distinct pain points. For each pain point return:
- text: clear description of the pain
- frequency: how many times mentioned (estimate 1-200)
- emotion_type: one of anger, frustration, disappointment, anxiety
- emotion_score: intensity 1-10
- example_quotes: 2-3 actual phrases from the text

Raw complaints:
{raw_text}

Return ONLY a JSON array, no markdown, no backticks, no other text:
[
    {{
        "text": "pain point description",
        "frequency": 45,
        "emotion_type": "frustration",
        "emotion_score": 7,
        "example_quotes": ["quote 1", "quote 2"]
    }}
]"""

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}],
        )

        extraction_text = ""
        for block in response.content:
            if block.type == "text":
                extraction_text += block.text

        try:
            pain_points_data = json.loads(extraction_text.strip())
        except json.JSONDecodeError:
            start = extraction_text.find("[")
            end = extraction_text.rfind("]") + 1
            if start != -1 and end > start:
                pain_points_data = json.loads(extraction_text[start:end])
            else:
                pain_points_data = []

        await db.pain_points.delete_many({"analysis_id": analysis_id})

        saved_pain_points = []
        for rank, pp in enumerate(pain_points_data, 1):
            pp_doc = {
                "_id": str(ObjectId()),
                "analysis_id": analysis_id,
                "text": pp.get("text", ""),
                "frequency": pp.get("frequency", 1),
                "emotion_score": pp.get("emotion_score", 5),
                "emotion_type": pp.get("emotion_type", "frustration"),
                "sources": pp.get("sources", []),
                "rank": rank,
                "example_quotes": pp.get("example_quotes", []),
            }
            await db.pain_points.insert_one(pp_doc)
            saved_pain_points.append(pp_doc)

        insight_narrative = await _generate_insight_narrative(saved_pain_points, analysis.get("topic", ""))

        response_items = [
            PainPointResponse(
                id=pp["_id"],
                analysis_id=pp["analysis_id"],
                text=pp["text"],
                frequency=pp["frequency"],
                emotion_score=pp["emotion_score"],
                emotion_type=pp["emotion_type"],
                sources=pp.get("sources", []),
                rank=pp["rank"],
                example_quotes=pp.get("example_quotes", []),
            )
            for pp in saved_pain_points
        ]

        return PainPointListResponse(
            pain_points=response_items,
            insight_narrative=insight_narrative,
            total_count=len(response_items),
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "Extraction failed", "detail": str(e)})


@router.get("/{analysis_id}", response_model=PainPointListResponse)
async def get_painpoints(analysis_id: str, current_user: dict = Depends(get_current_user)):
    try:
        db = get_database()

        analysis = await db.analyses.find_one({"_id": analysis_id, "user_id": current_user["id"]})
        if not analysis:
            raise HTTPException(status_code=404, detail={"error": "Not found", "detail": "Analysis not found"})

        cursor = db.pain_points.find({"analysis_id": analysis_id}).sort("rank", 1)
        pain_points = await cursor.to_list(length=50)

        response_items = [
            PainPointResponse(
                id=pp["_id"],
                analysis_id=pp["analysis_id"],
                text=pp["text"],
                frequency=pp["frequency"],
                emotion_score=pp["emotion_score"],
                emotion_type=pp["emotion_type"],
                sources=pp.get("sources", []),
                rank=pp["rank"],
                example_quotes=pp.get("example_quotes", []),
            )
            for pp in pain_points
        ]

        insight_narrative = await _generate_insight_narrative(
            [serialize_doc(pp) for pp in pain_points],
            analysis.get("topic", ""),
        )

        return PainPointListResponse(
            pain_points=response_items,
            insight_narrative=insight_narrative,
            total_count=len(response_items),
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "Failed to fetch pain points", "detail": str(e)})


@router.get("/{analysis_id}/narrative")
async def get_narrative(analysis_id: str, current_user: dict = Depends(get_current_user)):
    try:
        db = get_database()

        analysis = await db.analyses.find_one({"_id": analysis_id, "user_id": current_user["id"]})
        if not analysis:
            raise HTTPException(status_code=404, detail={"error": "Not found", "detail": "Analysis not found"})

        cursor = db.pain_points.find({"analysis_id": analysis_id}).sort("rank", 1)
        pain_points = await cursor.to_list(length=50)

        if not pain_points:
            return {"narrative": "No pain points found for this analysis yet."}

        narrative = await _generate_insight_narrative(
            [serialize_doc(pp) for pp in pain_points],
            analysis.get("topic", ""),
        )

        return {"narrative": narrative}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "Failed to generate narrative", "detail": str(e)})
