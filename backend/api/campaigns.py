import json
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
import anthropic
from database.mongodb import get_database, serialize_doc
from database.schemas import AdAssetResponse, AdAssetPackResponse
from api.auth import get_current_user

router = APIRouter(prefix="/api/campaigns", tags=["campaigns"])


@router.post("/generate", response_model=list[AdAssetPackResponse])
async def generate_campaign(
    analysis_id: str,
    language_override: str = None,
    current_user: dict = Depends(get_current_user),
):
    try:
        db = get_database()

        analysis = await db.analyses.find_one({"_id": analysis_id, "user_id": current_user["id"]})
        if not analysis:
            raise HTTPException(status_code=404, detail={"error": "Not found", "detail": "Analysis not found"})

        persona_cursor = db.personas.find({"analysis_id": analysis_id})
        personas = await persona_cursor.to_list(length=20)
        if not personas:
            raise HTTPException(status_code=400, detail={"error": "No data", "detail": "Generate personas before creating ad copy"})

        pp_cursor = db.pain_points.find({"analysis_id": analysis_id}).sort("rank", 1)
        pain_points = await pp_cursor.to_list(length=10)
        if not pain_points:
            raise HTTPException(status_code=400, detail={"error": "No data", "detail": "No pain points found"})

        client = anthropic.Anthropic()

        await db.ad_assets.delete_many({"analysis_id": analysis_id})

        all_packs = []

        for persona in personas:
            persona_pain_points = pain_points[:3]

            for pp in persona_pain_points:
                language = language_override or persona.get("language_preference", "hinglish")

                prompt = f"""You are an expert Indian marketing copywriter.

Persona: {persona['name']}, {persona.get('age_range', '25-40')} years old, {persona.get('occupation', 'professional')}
Core pain: {pp['text']}
Emotional state: {persona.get('emotional_state', 'frustrated')}
Language: {language}
Industry: {analysis.get('industry', '')}

Write ad copy for ALL these channels:
1. whatsapp: conversational, 2-3 lines, emoji ok
2. google_ad: headline (max 30 chars) + description (max 90 chars)
3. instagram: caption with hashtags, engaging, 2-3 lines
4. email_subject: A/B pair of subject lines, max 50 chars each
5. facebook: primary text, 100-150 words
6. landing_page: headline + subheading, benefit-focused

Rules:
- Use the EXACT frustration language from the pain point
- For hinglish: mix Hindi words naturally into English
- For hindi/bengali: write fully in that language
- Never use generic phrases like "best quality"
- Always end with a specific CTA
- Be specific to the Indian market

Return ONLY a JSON object with channel names as keys, no markdown, no backticks:
{{
    "whatsapp": "ad text here",
    "google_ad": "Headline|Description",
    "instagram": "caption here",
    "email_subject": "Subject A ||| Subject B",
    "facebook": "primary text here",
    "landing_page": "Headline - Subheading"
}}"""

                response = client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=2000,
                    messages=[{"role": "user", "content": prompt}],
                )

                response_text = ""
                for block in response.content:
                    if block.type == "text":
                        response_text += block.text

                try:
                    ads_data = json.loads(response_text.strip())
                except json.JSONDecodeError:
                    start = response_text.find("{")
                    end = response_text.rfind("}") + 1
                    if start != -1 and end > start:
                        ads_data = json.loads(response_text[start:end])
                    else:
                        ads_data = {}

                ads_for_pair = []
                for channel, content in ads_data.items():
                    ad_doc = {
                        "_id": str(ObjectId()),
                        "analysis_id": analysis_id,
                        "persona_id": persona["_id"],
                        "pain_point_id": pp["_id"],
                        "channel": channel,
                        "language": language,
                        "content": content,
                        "ctr_score": 5.0,
                        "emotional_trigger": pp.get("emotion_type", "frustration"),
                        "tone": persona.get("emotional_state", "empathetic"),
                    }
                    await db.ad_assets.insert_one(ad_doc)
                    ads_for_pair.append(ad_doc)

                pack = AdAssetPackResponse(
                    persona_id=persona["_id"],
                    persona_name=persona["name"],
                    pain_point=pp["text"],
                    ads=[
                        AdAssetResponse(
                            id=a["_id"],
                            analysis_id=a["analysis_id"],
                            persona_id=a["persona_id"],
                            pain_point_id=a["pain_point_id"],
                            channel=a["channel"],
                            language=a["language"],
                            content=a["content"],
                            ctr_score=a["ctr_score"],
                            emotional_trigger=a["emotional_trigger"],
                            tone=a["tone"],
                        )
                        for a in ads_for_pair
                    ],
                )
                all_packs.append(pack)

        return all_packs

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "Ad generation failed", "detail": str(e)})


@router.get("/{analysis_id}", response_model=list[AdAssetPackResponse])
async def get_ads(analysis_id: str, current_user: dict = Depends(get_current_user)):
    try:
        db = get_database()

        analysis = await db.analyses.find_one({"_id": analysis_id, "user_id": current_user["id"]})
        if not analysis:
            raise HTTPException(status_code=404, detail={"error": "Not found", "detail": "Analysis not found"})

        cursor = db.ad_assets.find({"analysis_id": analysis_id})
        ad_assets = await cursor.to_list(length=200)

        grouped = {}
        for ad in ad_assets:
            key = (ad["persona_id"], ad.get("pain_point_id", ""))
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(ad)

        packs = []
        for (persona_id, pp_id), ads in grouped.items():
            persona = await db.personas.find_one({"_id": persona_id})
            persona_name = persona.get("name", "Unknown") if persona else "Unknown"
            pp = await db.pain_points.find_one({"_id": pp_id})
            pp_text = pp.get("text", "") if pp else ""

            packs.append(
                AdAssetPackResponse(
                    persona_id=persona_id,
                    persona_name=persona_name,
                    pain_point=pp_text,
                    ads=[
                        AdAssetResponse(
                            id=a["_id"],
                            analysis_id=a["analysis_id"],
                            persona_id=a["persona_id"],
                            pain_point_id=a.get("pain_point_id", ""),
                            channel=a["channel"],
                            language=a.get("language", "english"),
                            content=a["content"],
                            ctr_score=a.get("ctr_score", 5.0),
                            emotional_trigger=a.get("emotional_trigger", ""),
                            tone=a.get("tone", ""),
                        )
                        for a in ads
                    ],
                )
            )

        return packs

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "Failed to fetch ads", "detail": str(e)})


@router.get("/{analysis_id}/persona/{persona_id}", response_model=list[AdAssetResponse])
async def get_ads_by_persona(
    analysis_id: str,
    persona_id: str,
    current_user: dict = Depends(get_current_user),
):
    try:
        db = get_database()

        analysis = await db.analyses.find_one({"_id": analysis_id, "user_id": current_user["id"]})
        if not analysis:
            raise HTTPException(status_code=404, detail={"error": "Not found", "detail": "Analysis not found"})

        cursor = db.ad_assets.find({"analysis_id": analysis_id, "persona_id": persona_id})
        ad_assets = await cursor.to_list(length=100)

        return [
            AdAssetResponse(
                id=a["_id"],
                analysis_id=a["analysis_id"],
                persona_id=a["persona_id"],
                pain_point_id=a.get("pain_point_id", ""),
                channel=a["channel"],
                language=a.get("language", "english"),
                content=a["content"],
                ctr_score=a.get("ctr_score", 5.0),
                emotional_trigger=a.get("emotional_trigger", ""),
                tone=a.get("tone", ""),
            )
            for a in ad_assets
        ]

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "Failed to fetch ads", "detail": str(e)})
