import json
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
import anthropic
from database.mongodb import get_database, serialize_doc
from database.schemas import PersonaResponse, PersonaListResponse
from api.auth import get_current_user

router = APIRouter(prefix="/api/personas", tags=["personas"])


@router.post("/generate", response_model=PersonaListResponse)
async def generate_personas(
    analysis_id: str,
    current_user: dict = Depends(get_current_user),
):
    try:
        db = get_database()

        analysis = await db.analyses.find_one({"_id": analysis_id, "user_id": current_user["id"]})
        if not analysis:
            raise HTTPException(status_code=404, detail={"error": "Not found", "detail": "Analysis not found"})

        cursor = db.pain_points.find({"analysis_id": analysis_id}).sort("rank", 1)
        pain_points = await cursor.to_list(length=50)
        if not pain_points:
            raise HTTPException(status_code=400, detail={"error": "No data", "detail": "Extract pain points before generating personas"})

        pain_summary = json.dumps(
            [{"text": p["text"], "frequency": p["frequency"], "emotion_type": p["emotion_type"],
              "emotion_score": p["emotion_score"], "rank": p["rank"]} for p in pain_points],
            indent=2,
        )

        client = anthropic.Anthropic()

        prompt = f"""You are a customer psychology expert.

Based on these pain points from real Indian customers in the {analysis.get('industry', '')} industry about "{analysis.get('topic', '')}":
{pain_summary}

Create 3 distinct buyer personas. For each persona return:
- name: descriptive label (e.g. "Busy Professional", "Budget-Conscious Parent")
- age_range: e.g. "25-35"
- occupation: typical job/role
- core_pain: which pain point affects them most (copy the exact text)
- emotional_state: how they feel when experiencing this
- revenue_potential: one of high, medium, low with one-line reason
- best_channels: top 2 channels from [whatsapp, google, instagram, email, facebook, landing_page]
- language_preference: one of english, hinglish, hindi, bengali
- what_they_want: one sentence — their ideal outcome

Return ONLY a JSON array, no markdown, no backticks, no other text:
[
    {{
        "name": "Persona Name",
        "age_range": "25-35",
        "occupation": "Job title",
        "core_pain": "pain point text",
        "emotional_state": "how they feel",
        "revenue_potential": "high",
        "revenue_reason": "why",
        "best_channels": ["whatsapp", "instagram"],
        "language_preference": "hinglish",
        "what_they_want": "ideal outcome sentence"
    }}
]"""

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}],
        )

        response_text = ""
        for block in response.content:
            if block.type == "text":
                response_text += block.text

        try:
            personas_data = json.loads(response_text.strip())
        except json.JSONDecodeError:
            start = response_text.find("[")
            end = response_text.rfind("]") + 1
            if start != -1 and end > start:
                personas_data = json.loads(response_text[start:end])
            else:
                personas_data = []

        await db.personas.delete_many({"analysis_id": analysis_id})

        saved_personas = []
        for persona in personas_data:
            pain_point_ids = []
            for pp in pain_points:
                if pp["text"] in persona.get("core_pain", "") or persona.get("core_pain", "") in pp["text"]:
                    pain_point_ids.append(pp["_id"])

            persona_doc = {
                "_id": str(ObjectId()),
                "analysis_id": analysis_id,
                "name": persona.get("name", "Unknown"),
                "age_range": persona.get("age_range", "25-40"),
                "occupation": persona.get("occupation", "Professional"),
                "pain_points": pain_point_ids,
                "revenue_potential": persona.get("revenue_potential", "medium"),
                "best_channels": persona.get("best_channels", ["whatsapp"]),
                "language_preference": persona.get("language_preference", "hinglish"),
                "core_pain": persona.get("core_pain", ""),
                "emotional_state": persona.get("emotional_state", ""),
                "what_they_want": persona.get("what_they_want", ""),
            }
            await db.personas.insert_one(persona_doc)
            saved_personas.append(persona_doc)

        response_items = [
            PersonaResponse(
                id=p["_id"],
                analysis_id=p["analysis_id"],
                name=p["name"],
                age_range=p["age_range"],
                occupation=p["occupation"],
                pain_points=p["pain_points"],
                revenue_potential=p["revenue_potential"],
                best_channels=p["best_channels"],
                language_preference=p["language_preference"],
                core_pain=p.get("core_pain", ""),
                emotional_state=p.get("emotional_state", ""),
                what_they_want=p.get("what_they_want", ""),
            )
            for p in saved_personas
        ]

        return PersonaListResponse(personas=response_items, total_count=len(response_items))

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "Persona generation failed", "detail": str(e)})


@router.get("/{analysis_id}", response_model=PersonaListResponse)
async def get_personas(analysis_id: str, current_user: dict = Depends(get_current_user)):
    try:
        db = get_database()

        analysis = await db.analyses.find_one({"_id": analysis_id, "user_id": current_user["id"]})
        if not analysis:
            raise HTTPException(status_code=404, detail={"error": "Not found", "detail": "Analysis not found"})

        cursor = db.personas.find({"analysis_id": analysis_id})
        personas = await cursor.to_list(length=20)

        response_items = [
            PersonaResponse(
                id=p["_id"],
                analysis_id=p["analysis_id"],
                name=p["name"],
                age_range=p["age_range"],
                occupation=p["occupation"],
                pain_points=p.get("pain_points", []),
                revenue_potential=p["revenue_potential"],
                best_channels=p["best_channels"],
                language_preference=p["language_preference"],
                core_pain=p.get("core_pain", ""),
                emotional_state=p.get("emotional_state", ""),
                what_they_want=p.get("what_they_want", ""),
            )
            for p in personas
        ]

        return PersonaListResponse(personas=response_items, total_count=len(response_items))

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "Failed to fetch personas", "detail": str(e)})
