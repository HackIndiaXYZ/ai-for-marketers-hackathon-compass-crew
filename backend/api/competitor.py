import json
from datetime import datetime
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
import anthropic
from database.mongodb import get_database, serialize_doc
from database.schemas import CompetitorRequest, CompetitorResponse
from api.auth import get_current_user

router = APIRouter(prefix="/api/competitor", tags=["competitor"])


@router.post("/analyze", response_model=CompetitorResponse)
async def analyze_competitor(
    request: CompetitorRequest,
    current_user: dict = Depends(get_current_user),
):
    try:
        db = get_database()

        analysis = await db.analyses.find_one({"_id": request.analysis_id, "user_id": current_user["id"]})
        if not analysis:
            raise HTTPException(status_code=404, detail={"error": "Not found", "detail": "Analysis not found"})

        client = anthropic.Anthropic()

        search_prompt = f"""Search for complaints and negative reviews about "{request.competitor_name}" in India.

Use web_search to find:
1. {request.competitor_name} complaints reviews india
2. {request.competitor_name} negative feedback problems

Extract the key complaints and weaknesses mentioned by customers.

Return ONLY a JSON object, no markdown, no backticks:
{{
    "weaknesses": ["weakness 1 description", "weakness 2 description", ...],
    "raw_complaints": ["complaint 1", "complaint 2", ...]
}}"""

        search_response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=3000,
            tools=[{"type": "web_search_20250305", "name": "web_search"}],
            messages=[{"role": "user", "content": search_prompt}],
        )

        search_text = ""
        for block in search_response.content:
            if block.type == "text":
                search_text += block.text

        try:
            search_result = json.loads(search_text.strip())
        except json.JSONDecodeError:
            start = search_text.find("{")
            end = search_text.rfind("}") + 1
            if start != -1 and end > start:
                search_result = json.loads(search_text[start:end])
            else:
                search_result = {"weaknesses": [], "raw_complaints": []}

        weaknesses = search_result.get("weaknesses", [])
        raw_complaints = search_result.get("raw_complaints", [])

        ad_prompt = f"""You are a competitive intelligence expert and marketing copywriter.

Competitor: {request.competitor_name}
Their weaknesses (from real customer complaints):
{json.dumps(weaknesses, indent=2)}

Raw customer complaints:
{json.dumps(raw_complaints[:10], indent=2)}

For each weakness, generate an attack ad that:
- Highlights this competitor weakness WITHOUT naming them directly
- Implies the problem and positions us as the solution
- Uses emotional language from the actual complaints
- Is specific to the Indian market
- Is suitable for digital advertising

Return ONLY a JSON array of ad copies, no markdown, no backticks:
[
    "Ad copy for weakness 1...",
    "Ad copy for weakness 2..."
]"""

        ad_response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2000,
            messages=[{"role": "user", "content": ad_prompt}],
        )

        ad_text = ""
        for block in ad_response.content:
            if block.type == "text":
                ad_text += block.text

        try:
            opportunity_ads = json.loads(ad_text.strip())
        except json.JSONDecodeError:
            start = ad_text.find("[")
            end = ad_text.rfind("]") + 1
            if start != -1 and end > start:
                opportunity_ads = json.loads(ad_text[start:end])
            else:
                opportunity_ads = []

        competitor_id = str(ObjectId())
        competitor_doc = {
            "_id": competitor_id,
            "analysis_id": request.analysis_id,
            "competitor_name": request.competitor_name,
            "weaknesses": weaknesses,
            "opportunity_ads": opportunity_ads,
            "created_at": datetime.utcnow(),
        }

        await db.competitors.insert_one(competitor_doc)

        return CompetitorResponse(
            id=competitor_id,
            analysis_id=request.analysis_id,
            competitor_name=request.competitor_name,
            weaknesses=weaknesses,
            opportunity_ads=opportunity_ads,
            created_at=competitor_doc["created_at"],
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "Competitor analysis failed", "detail": str(e)})


@router.get("/{analysis_id}", response_model=list[CompetitorResponse])
async def get_competitor_analyses(
    analysis_id: str,
    current_user: dict = Depends(get_current_user),
):
    try:
        db = get_database()

        analysis = await db.analyses.find_one({"_id": analysis_id, "user_id": current_user["id"]})
        if not analysis:
            raise HTTPException(status_code=404, detail={"error": "Not found", "detail": "Analysis not found"})

        cursor = db.competitors.find({"analysis_id": analysis_id})
        competitors = await cursor.to_list(length=20)

        return [
            CompetitorResponse(
                id=c["_id"],
                analysis_id=c["analysis_id"],
                competitor_name=c["competitor_name"],
                weaknesses=c.get("weaknesses", []),
                opportunity_ads=c.get("opportunity_ads", []),
                created_at=c["created_at"],
            )
            for c in competitors
        ]

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "Failed to fetch competitor analyses", "detail": str(e)})
