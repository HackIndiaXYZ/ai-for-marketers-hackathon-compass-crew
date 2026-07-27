import json
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import anthropic
from database.mongodb import get_database, serialize_doc
from database.schemas import TrendResponse, SeasonalRequest
from api.auth import get_current_user

router = APIRouter(prefix="/api/trends", tags=["trends"])


@router.get("/{analysis_id}", response_model=TrendResponse)
async def get_trends(analysis_id: str, current_user: dict = Depends(get_current_user)):
    try:
        db = get_database()

        analysis = await db.analyses.find_one({"_id": analysis_id, "user_id": current_user["id"]})
        if not analysis:
            raise HTTPException(status_code=404, detail={"error": "Not found", "detail": "Analysis not found"})

        cursor = db.pain_points.find({"analysis_id": analysis_id}).sort("rank", 1)
        pain_points = await cursor.to_list(length=50)

        if not pain_points:
            raise HTTPException(status_code=400, detail={"error": "No data", "detail": "No pain points found for trend analysis"})

        pain_summary = json.dumps(
            [{"text": p["text"], "frequency": p["frequency"], "emotion_type": p.get("emotion_type", ""),
              "emotion_score": p.get("emotion_score", 5), "rank": p.get("rank", 0)}
             for p in pain_points],
            indent=2,
        )

        client = anthropic.Anthropic()

        prompt = f"""You are a market trends analyst for the Indian market.

Based on these pain points from the {analysis.get('industry', '')} industry about "{analysis.get('topic', '')}":
{pain_summary}

Analyze trends and provide:
1. Which pains are GROWING vs DECLINING in mentions (based on frequency and market context)
2. Seasonal patterns (festivals like Diwali, Holi, monsoon, summer, etc.)
3. Which emerging pain is UNDERSERVED by competitors
4. Opportunity score 1-10 for each pain point

Return ONLY a JSON object, no markdown, no backticks:
{{
    "trending_pains": [
        {{
            "pain": "pain point text",
            "trend": "growing/declining/stable",
            "reason": "why this trend",
            "opportunity_score": 8
        }}
    ],
    "seasonal_insight": "description of seasonal patterns relevant to this industry in India",
    "opportunity_scores": {{
        "pain_point_1": 8,
        "pain_point_2": 6
    }}
}}"""

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=3000,
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
                    "trending_pains": [{"pain": pp["text"], "trend": "stable", "reason": "Consistent mention", "opportunity_score": 5} for pp in pain_points[:5]],
                    "seasonal_insight": "Seasonal patterns vary by industry.",
                    "opportunity_scores": {pp["text"]: 5 for pp in pain_points[:5]},
                }

        return TrendResponse(
            analysis_id=analysis_id,
            trending_pains=result.get("trending_pains", []),
            seasonal_insight=result.get("seasonal_insight", ""),
            opportunity_scores=result.get("opportunity_scores", {}),
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "Trend analysis failed", "detail": str(e)})


@router.post("/seasonal")
async def seasonal_campaign(
    request: SeasonalRequest,
    current_user: dict = Depends(get_current_user),
):
    try:
        client = anthropic.Anthropic()

        prompt = f"""You are a seasonal marketing expert for Indian businesses.

Industry: {request.industry}
Upcoming festival/season: {request.festival_or_season}
Known pain points: {json.dumps(request.pain_points, indent=2)}

Provide:
1. Which pain points become MORE ACUTE during {request.festival_or_season}
2. A festival-specific campaign hook for the top pain point
3. Specific timing recommendations
4. Channel recommendations for this season

Return ONLY a JSON object, no markdown, no backticks:
{{
    "acute_pains": ["pain 1 becomes worse because..."],
    "campaign_hook": "Festival-specific ad angle and headline",
    "timing": "when to launch and run this campaign",
    "channels": ["best channels for this season"]
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
                    "acute_pains": [],
                    "campaign_hook": f"Seasonal campaign for {request.festival_or_season}",
                    "timing": "2 weeks before the event",
                    "channels": ["whatsapp", "instagram"],
                }

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "Seasonal analysis failed", "detail": str(e)})
