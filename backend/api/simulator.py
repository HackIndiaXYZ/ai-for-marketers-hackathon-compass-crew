import json
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
import anthropic
from database.mongodb import get_database, serialize_doc
from database.schemas import SimulatorRequest, SimulatorResponse
from api.auth import get_current_user

router = APIRouter(prefix="/api/simulator", tags=["simulator"])


@router.post("/run", response_model=SimulatorResponse)
async def run_simulation(
    request: SimulatorRequest,
    current_user: dict = Depends(get_current_user),
):
    try:
        db = get_database()

        analysis = await db.analyses.find_one({"_id": request.analysis_id, "user_id": current_user["id"]})
        if not analysis:
            raise HTTPException(status_code=404, detail={"error": "Not found", "detail": "Analysis not found"})

        ad_cursor = db.ad_assets.find({"analysis_id": request.analysis_id})
        ad_assets = await ad_cursor.to_list(length=200)

        persona_cursor = db.personas.find({"analysis_id": request.analysis_id})
        personas = await persona_cursor.to_list(length=20)

        best_ctr = 5.0
        best_channel = request.selected_channels[0] if request.selected_channels else "whatsapp"
        target_persona = personas[0]["name"] if personas else "Unknown"

        for ad in ad_assets:
            if ad.get("ctr_score", 0) > best_ctr:
                best_ctr = ad["ctr_score"]
                best_channel = ad["channel"]

        client = anthropic.Anthropic()

        prompt = f"""You are a performance marketing simulator for Indian SMBs.

Simulate a {request.duration_days}-day campaign for an Indian business with budget ₹{request.budget:,.0f}.

Selected channels: {json.dumps(request.selected_channels)}
Top ad variant CTR score: {best_ctr}/10
Best channel: {best_channel}
Target persona: {target_persona}
Industry: {analysis.get('industry', '')}

Base your estimates on realistic Indian SMB benchmarks:
- WhatsApp CTR avg 4-8%, conversion rate 2-5%
- Google Search CTR 2-4%, conversion rate 3-7%
- Instagram CTR 0.5-1.5%, conversion rate 1-3%
- Email open rate 15-25%, click rate 2-5%, conversion 1-3%
- Facebook CTR 0.5-2%, conversion rate 1-4%
- Landing page conversion rate 5-15%

Calculate daily projections with:
- Learning phase (days 1-3): 50% performance
- Ramp phase (days 4-7): 75% performance
- Optimized phase (days 8+): 100% performance
- Assume average order value of ₹500-2000 depending on industry

Return ONLY a JSON object, no markdown, no backticks:
{{
    "daily_projection": {{
        "day_1": cumulative_conversions,
        "day_2": cumulative_conversions,
        ...
    }},
    "total_conversions": integer,
    "total_revenue": INR estimate,
    "roi_percentage": float,
    "best_performing_day": day_number,
    "recommended_variant": "which ad to lead with",
    "confidence_level": "high/medium/low",
    "confidence_reason": "why this confidence level"
}}"""

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
            result = json.loads(response_text.strip())
        except json.JSONDecodeError:
            start = response_text.find("{")
            end = response_text.rfind("}") + 1
            if start != -1 and end > start:
                result = json.loads(response_text[start:end])
            else:
                daily = {}
                base = int(request.budget * 0.002)
                for day in range(1, min(request.duration_days + 1, 31)):
                    multiplier = 0.5 if day <= 3 else (0.75 if day <= 7 else 1.0)
                    daily[f"day_{day}"] = int(base * multiplier * day)
                total = daily.get(f"day_{min(request.duration_days, 30)}", base * 30)
                revenue = total * 1000
                result = {
                    "daily_projection": daily,
                    "total_conversions": total,
                    "total_revenue": revenue,
                    "roi_percentage": ((revenue - request.budget) / request.budget) * 100,
                    "best_performing_day": min(request.duration_days, 30),
                    "recommended_variant": best_channel,
                    "confidence_level": "medium",
                    "confidence_reason": "Estimated based on industry averages",
                }

        return SimulatorResponse(
            analysis_id=request.analysis_id,
            daily_projection=result.get("daily_projection", {}),
            total_conversions=result.get("total_conversions", 0),
            total_revenue=result.get("total_revenue", 0.0),
            roi_percentage=result.get("roi_percentage", 0.0),
            best_performing_day=result.get("best_performing_day", 1),
            recommended_variant=result.get("recommended_variant", best_channel),
            confidence_level=result.get("confidence_level", "medium"),
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "Simulation failed", "detail": str(e)})


@router.get("/history/{user_id}", response_model=list[SimulatorResponse])
async def get_simulation_history(
    user_id: str,
    current_user: dict = Depends(get_current_user),
):
    try:
        if user_id != current_user["id"]:
            raise HTTPException(status_code=403, detail={"error": "Forbidden", "detail": "Cannot access other user's history"})

        db = get_database()
        cursor = db.campaigns.find({"user_id": user_id}).sort("created_at", -1).limit(5)
        campaigns = await cursor.to_list(length=5)

        results = []
        for campaign in campaigns:
            results.append(
                SimulatorResponse(
                    analysis_id=campaign.get("analysis_id", ""),
                    daily_projection=campaign.get("simulation_data", {}).get("daily_projection", {}),
                    total_conversions=campaign.get("simulation_data", {}).get("total_conversions", 0),
                    total_revenue=campaign.get("simulation_data", {}).get("total_revenue", 0.0),
                    roi_percentage=campaign.get("simulation_data", {}).get("roi_percentage", 0.0),
                    best_performing_day=campaign.get("simulation_data", {}).get("best_performing_day", 1),
                    recommended_variant=campaign.get("simulation_data", {}).get("recommended_variant", ""),
                    confidence_level=campaign.get("simulation_data", {}).get("confidence_level", "medium"),
                )
            )

        return results

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "Failed to fetch history", "detail": str(e)})
