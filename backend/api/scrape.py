import os
import json
from datetime import datetime
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from fastapi.background import BackgroundTasks
import anthropic
from serpapi import GoogleSearch
from database.mongodb import get_database, serialize_doc
from database.schemas import AnalysisCreateRequest, AnalysisResponse, AnalysisStatusResponse
from api.auth import get_current_user

router = APIRouter(prefix="/api/scrape", tags=["scrape"])

SERPAPI_KEY = os.getenv("SERPAPI_KEY", "ba48d67deabdf71f6d3eaadff413f731cdf621bbd573644dac1e987f9b294739")


def _search_serpapi(query: str) -> list[dict]:
    params = {
        "q": query,
        "api_key": SERPAPI_KEY,
        "engine": "google",
        "num": 10,
        "gl": "in",
        "hl": "en",
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    return [
        {"title": r.get("title", ""), "snippet": r.get("snippet", ""), "link": r.get("link", "")}
        for r in results.get("organic_results", [])
    ]


def _scrape_complaints(topic: str) -> str:
    queries = [
        f"{topic} complaints problems india reddit",
        f"{topic} negative reviews india",
        f"{topic} frustrated customers quora",
        f"site:mouthshut.com {topic} review",
    ]

    all_snippets = []
    all_sources = []

    for query in queries:
        try:
            results = _search_serpapi(query)
            for r in results:
                if r["snippet"]:
                    all_snippets.append(r["snippet"])
                if r["link"]:
                    all_sources.append(r["link"])
        except Exception:
            continue

    combined = "\n\n".join(all_snippets)
    source_list = "\n".join(all_sources)
    return f"COMPLAINT SNIPPETS:\n{combined}\n\nSOURCES:\n{source_list}"


async def _run_analysis_pipeline(analysis_id: str, topic: str, industry: str, language: str):
    db = get_database()
    try:
        await db.analyses.update_one(
            {"_id": analysis_id},
            {"$set": {"status": "processing", "progress": 10}},
        )

        raw_text = _scrape_complaints(topic)

        if not raw_text or len(raw_text.strip()) < 50:
            raise Exception("SerpAPI returned no useful data")

        await db.analyses.update_one(
            {"_id": analysis_id},
            {"$set": {"progress": 40, "raw_data": raw_text}},
        )

        client = anthropic.Anthropic()

        extraction_prompt = f"""You are a marketing intelligence analyst.

From these real customer complaints about "{topic}" in the {industry} industry, extract 5-8 distinct pain points.

Raw complaint data:
{raw_text}

For each pain point return:
- text: clear description of the pain
- frequency: how many times mentioned (estimate 1-200)
- emotion_type: one of anger, frustration, disappointment, anxiety
- emotion_score: intensity 1-10
- example_quotes: 2-3 actual phrases from the text
- sources: list of relevant URLs if available

Return ONLY a JSON array, no markdown, no backticks, no other text:
[
    {{
        "text": "pain point description",
        "frequency": 45,
        "emotion_type": "frustration",
        "emotion_score": 7,
        "example_quotes": ["quote 1", "quote 2"],
        "sources": ["url1"]
    }}
]"""

        extraction_response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4000,
            messages=[{"role": "user", "content": extraction_prompt}],
        )

        extraction_text = ""
        for block in extraction_response.content:
            if block.type == "text":
                extraction_text += block.text

        await db.analyses.update_one(
            {"_id": analysis_id},
            {"$set": {"progress": 70}},
        )

        try:
            pain_points_data = json.loads(extraction_text.strip())
        except json.JSONDecodeError:
            start = extraction_text.find("[")
            end = extraction_text.rfind("]") + 1
            if start != -1 and end > start:
                pain_points_data = json.loads(extraction_text[start:end])
            else:
                pain_points_data = []

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

        await db.analyses.update_one(
            {"_id": analysis_id},
            {
                "$set": {
                    "status": "complete",
                    "progress": 100,
                    "completed_at": datetime.utcnow(),
                }
            },
        )

    except Exception as e:
        await db.analyses.update_one(
            {"_id": analysis_id},
            {"$set": {"status": "failed", "progress": 0}},
        )


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze(
    request: AnalysisCreateRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user),
):
    try:
        db = get_database()

        analysis_id = str(ObjectId())
        analysis_doc = {
            "_id": analysis_id,
            "user_id": current_user["id"],
            "topic": request.topic,
            "industry": request.industry,
            "status": "pending",
            "created_at": datetime.utcnow(),
            "completed_at": None,
            "raw_data": "",
            "progress": 0,
        }

        await db.analyses.insert_one(analysis_doc)

        background_tasks.add_task(
            _run_analysis_pipeline,
            analysis_id,
            request.topic,
            request.industry,
            request.language,
        )

        return AnalysisResponse(
            id=analysis_id,
            user_id=current_user["id"],
            topic=request.topic,
            industry=request.industry,
            status="pending",
            created_at=analysis_doc["created_at"],
            progress=0,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "Analysis failed to start", "detail": str(e)})


@router.get("/status/{analysis_id}", response_model=AnalysisStatusResponse)
async def get_status(analysis_id: str, current_user: dict = Depends(get_current_user)):
    try:
        db = get_database()
        analysis = await db.analyses.find_one({"_id": analysis_id, "user_id": current_user["id"]})
        if not analysis:
            raise HTTPException(status_code=404, detail={"error": "Not found", "detail": "Analysis not found"})

        analysis = serialize_doc(analysis)
        return AnalysisStatusResponse(
            id=analysis["id"],
            status=analysis["status"],
            progress=analysis.get("progress", 0),
            topic=analysis["topic"],
            created_at=analysis["created_at"],
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "Failed to get status", "detail": str(e)})
