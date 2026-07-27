import json
from fastapi import APIRouter, Depends, HTTPException
import anthropic
from database.mongodb import get_database, serialize_doc
from database.schemas import InsightResponse
from api.auth import get_current_user

router = APIRouter(prefix="/api/insights", tags=["insights"])


@router.get("/{analysis_id}", response_model=InsightResponse)
async def get_insights(analysis_id: str, current_user: dict = Depends(get_current_user)):
    try:
        db = get_database()

        analysis = await db.analyses.find_one({"_id": analysis_id, "user_id": current_user["id"]})
        if not analysis:
            raise HTTPException(status_code=404, detail={"error": "Not found", "detail": "Analysis not found"})

        pp_cursor = db.pain_points.find({"analysis_id": analysis_id}).sort("rank", 1)
        pain_points = await pp_cursor.to_list(length=50)

        persona_cursor = db.personas.find({"analysis_id": analysis_id})
        personas = await persona_cursor.to_list(length=20)

        competitor_cursor = db.competitors.find({"analysis_id": analysis_id})
        competitors = await competitor_cursor.to_list(length=20)

        aggregated = {
            "topic": analysis.get("topic", ""),
            "industry": analysis.get("industry", ""),
            "pain_points": [
                {"text": p["text"], "frequency": p["frequency"], "emotion_type": p.get("emotion_type", ""),
                 "emotion_score": p.get("emotion_score", 5), "rank": p.get("rank", 0)}
                for p in pain_points
            ],
            "personas": [
                {"name": p["name"], "age_range": p.get("age_range", ""), "occupation": p.get("occupation", ""),
                 "revenue_potential": p.get("revenue_potential", "medium"),
                 "best_channels": p.get("best_channels", []),
                 "core_pain": p.get("core_pain", "")}
                for p in personas
            ],
            "competitor_weaknesses": [
                {"name": c.get("competitor_name", ""), "weaknesses": c.get("weaknesses", [])}
                for c in competitors
            ],
        }

        client = anthropic.Anthropic()

        prompt = f"""You are a senior marketing strategist.

Data for {analysis.get('topic', '')} in the {analysis.get('industry', '')} industry:
{json.dumps(aggregated, indent=2)}

Write a strategic marketing brief with:
1. top_opportunity: single biggest pain to target (one sentence)
2. best_persona: which customer to focus on first and why (one sentence)
3. recommended_channel: where to spend first rupee and why (one sentence)
4. competitor_gap: what competitors are missing (one sentence)
5. narrative: 4-sentence plain English summary a small business owner can understand immediately

Return ONLY a JSON object, no markdown, no backticks:
{{
    "top_opportunity": "pain point description",
    "best_persona": "persona name and reason",
    "recommended_channel": "channel and reason",
    "competitor_gap": "gap description",
    "narrative": "4-sentence plain English summary"
}}"""

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}],
        )

        response_text = ""
        for block in response.content:
            if block.type == "text":
                response_text += block.text

        try:
            result = json.loads(response_text.strip())
        except json.JSONDecodeError:
            start = response_text.find("{")
            end = response_text.rfind("}") + 1
            if start != -1 and end > start:
                result = json.loads(response_text[start:end])
            else:
                result = {
                    "top_opportunity": "Customer pain points identified",
                    "best_persona": "Target persona identified",
                    "recommended_channel": "Digital channels recommended",
                    "competitor_gap": "Opportunity exists in the market",
                    "narrative": f"Analysis of {analysis.get('topic', '')} reveals significant customer pain points in the {analysis.get('industry', '')} industry. Focus on the highest-frequency pain point with empathetic, solution-focused messaging.",
                }

        return InsightResponse(
            analysis_id=analysis_id,
            narrative=result.get("narrative", ""),
            top_pain=result.get("top_opportunity", ""),
            best_persona=result.get("best_persona", ""),
            recommended_channel=result.get("recommended_channel", ""),
            competitor_gap=result.get("competitor_gap", ""),
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "Failed to generate insights", "detail": str(e)})


@router.post("/narrative")
async def get_narrative(
    analysis_id: str,
    current_user: dict = Depends(get_current_user),
):
    try:
        db = get_database()

        analysis = await db.analyses.find_one({"_id": analysis_id, "user_id": current_user["id"]})
        if not analysis:
            raise HTTPException(status_code=404, detail={"error": "Not found", "detail": "Analysis not found"})

        pp_cursor = db.pain_points.find({"analysis_id": analysis_id}).sort("rank", 1)
        pain_points = await pp_cursor.to_list(length=10)

        persona_cursor = db.personas.find({"analysis_id": analysis_id})
        personas = await persona_cursor.to_list(length=10)

        data_summary = {
            "topic": analysis.get("topic", ""),
            "top_pain": pain_points[0]["text"] if pain_points else "N/A",
            "top_pain_frequency": pain_points[0].get("frequency", 0) if pain_points else 0,
            "top_persona": personas[0]["name"] if personas else "N/A",
            "top_persona_channels": personas[0].get("best_channels", []) if personas else [],
        }

        client = anthropic.Anthropic()

        prompt = f"""You are a senior marketing strategist writing a brief for a small business owner.

Analysis data:
{json.dumps(data_summary, indent=2)}

Write a 4-sentence plain English narrative that explains:
1. What the biggest customer pain is
2. Who the ideal customer is
3. Where to reach them first
4. Why this is an opportunity

Write like you're talking to a smart friend who runs a small business. No jargon. Max 4 sentences. Return ONLY the narrative text, no JSON, no markdown."""

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )

        narrative = ""
        for block in response.content:
            if block.type == "text":
                narrative += block.text

        return {"narrative": narrative.strip()}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "Failed to generate narrative", "detail": str(e)})
