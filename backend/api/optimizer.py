import json
from fastapi import APIRouter, Depends, HTTPException
import anthropic
from database.mongodb import get_database, serialize_doc
from database.schemas import OptimizerRequest, OptimizerResponse
from api.auth import get_current_user

router = APIRouter(prefix="/api/optimizer", tags=["optimizer"])


@router.post("/score", response_model=OptimizerResponse)
async def score_ads(
    request: OptimizerRequest,
    current_user: dict = Depends(get_current_user),
):
    try:
        db = get_database()

        analysis = await db.analyses.find_one({"_id": request.analysis_id, "user_id": current_user["id"]})
        if not analysis:
            raise HTTPException(status_code=404, detail={"error": "Not found", "detail": "Analysis not found"})

        cursor = db.ad_assets.find({"analysis_id": request.analysis_id})
        ad_assets = await cursor.to_list(length=200)
        if not ad_assets:
            raise HTTPException(status_code=400, detail={"error": "No data", "detail": "Generate ad copy before scoring"})

        ad_summaries = []
        for ad in ad_assets[:15]:
            persona = await db.personas.find_one({"_id": ad["persona_id"]})
            persona_name = persona.get("name", "Unknown") if persona else "Unknown"
            ad_summaries.append({
                "id": ad["_id"],
                "channel": ad["channel"],
                "persona": persona_name,
                "content": ad["content"][:200],
                "language": ad.get("language", "english"),
            })

        client = anthropic.Anthropic()

        prompt = f"""You are a performance marketing expert specializing in Indian digital advertising.

Total budget: ₹{request.budget:,.0f}

Score each ad variant (0-10) on predicted CTR based on:
- Emotional resonance with target persona
- Specificity vs generic language
- CTA clarity and urgency
- Channel fit for Indian market context
- Language appropriateness

Ad variants:
{json.dumps(ad_summaries, indent=2)}

Then recommend budget allocation across top variants for total budget of ₹{request.budget:,.0f}.

Also estimate:
- projected_ctr: percentage (realistic for Indian market)
- projected_conversions: per month at this budget
- roi_estimate: revenue return in INR

Return ONLY a JSON object, no markdown, no backticks:
{{
    "variant_scores": [
        {{
            "ad_id": "id",
            "channel": "channel",
            "persona": "persona name",
            "ctr_score": 7.5,
            "reasoning": "why this score"
        }}
    ],
    "budget_split": {{
        "ad_id_1": 40,
        "ad_id_2": 30,
        "ad_id_3": 30
    }},
    "projected_ctr": 3.5,
    "projected_conversions": 150,
    "roi_estimate": 75000,
    "narrative": "brief strategic recommendation"
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
                result = {
                    "variant_scores": [],
                    "budget_split": {},
                    "projected_ctr": 2.0,
                    "projected_conversions": 0,
                    "roi_estimate": 0,
                    "narrative": "Unable to generate scoring at this time.",
                }

        for score in result.get("variant_scores", []):
            ad_id = score.get("ad_id", "")
            ctr = score.get("ctr_score", 5.0)
            if ad_id:
                await db.ad_assets.update_one(
                    {"_id": ad_id},
                    {"$set": {"ctr_score": ctr}},
                )

        return OptimizerResponse(
            variant_scores=result.get("variant_scores", []),
            budget_split=result.get("budget_split", {}),
            projected_ctr=result.get("projected_ctr", 0.0),
            projected_conversions=result.get("projected_conversions", 0),
            roi_estimate=result.get("roi_estimate", 0.0),
            narrative=result.get("narrative", ""),
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "Scoring failed", "detail": str(e)})


@router.get("/report/{analysis_id}", response_model=OptimizerResponse)
async def get_optimization_report(
    analysis_id: str,
    current_user: dict = Depends(get_current_user),
):
    try:
        db = get_database()

        analysis = await db.analyses.find_one({"_id": analysis_id, "user_id": current_user["id"]})
        if not analysis:
            raise HTTPException(status_code=404, detail={"error": "Not found", "detail": "Analysis not found"})

        cursor = db.ad_assets.find({"analysis_id": analysis_id})
        ad_assets = await cursor.to_list(length=200)

        variant_scores = []
        budget_split = {}
        for ad in ad_assets:
            variant_scores.append({
                "ad_id": ad["_id"],
                "channel": ad["channel"],
                "ctr_score": ad.get("ctr_score", 5.0),
            })
            budget_split[ad["_id"]] = 100 // max(len(ad_assets), 1)

        return OptimizerResponse(
            variant_scores=variant_scores,
            budget_split=budget_split,
            projected_ctr=2.5,
            projected_conversions=0,
            roi_estimate=0.0,
            narrative="Report generated from stored ad assets. Run /score for fresh AI-powered analysis.",
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "Failed to fetch report", "detail": str(e)})
