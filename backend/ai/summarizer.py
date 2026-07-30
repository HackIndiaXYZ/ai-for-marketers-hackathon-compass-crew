"""
Summarizer Utility
------------------

Responsibilities
----------------
- Compress customer reviews
- Remove duplicate information
- Extract key topics
- Preserve representative customer quotes
- Reduce Gemini token usage
- Support hierarchical chunk summarization
"""

from __future__ import annotations

from typing import List, Dict, Any

from backend.ai.gemini import gemini


MAX_CHUNK_SIZE = 100


class ReviewSummarizer:
    """
    Review summarization utility.

    Workflow

    Reviews
        ↓
    Chunk Reviews
        ↓
    Summarize Each Chunk
        ↓
    Merge Chunk Summaries
        ↓
    Final Master Summary
    """

    # -----------------------------------------------------
    # Public API
    # -----------------------------------------------------

    def summarize_reviews(
        self,
        reviews: List[Any]
    ) -> Dict[str, Any]:
        """
        Summarize customer reviews.

        Automatically performs hierarchical summarization
        for large review collections.
        """

        if not reviews:
            return self._empty_summary()

        unique_reviews = self._deduplicate(reviews)

        statistics = {
            "total_reviews": len(reviews),
            "duplicates_removed": len(reviews) - len(unique_reviews),
            "unique_reviews": len(unique_reviews),
        }

        if len(unique_reviews) <= MAX_CHUNK_SIZE:

            summary = self._summarize_chunk(unique_reviews)

            summary["statistics"] = statistics

            return summary

        chunk_summaries = []

        chunks = [
            unique_reviews[i:i + MAX_CHUNK_SIZE]
            for i in range(0, len(unique_reviews), MAX_CHUNK_SIZE)
        ]

        for chunk in chunks:
            chunk_summaries.append(
                self._summarize_chunk(chunk)
            )

        final_summary = self._merge_summaries(chunk_summaries)

        final_summary["statistics"] = statistics

        return final_summary

    # -----------------------------------------------------
    # Helpers
    # -----------------------------------------------------

    def _deduplicate(
        self,
        reviews: List[Any]
    ) -> List[Any]:

        seen = set()
        unique = []

        for review in reviews:

            if isinstance(review, dict):
                text = review.get("review") or review.get("text", "")
            else:
                text = str(review)

            normalized = text.strip().lower()

            if normalized not in seen:
                seen.add(normalized)
                unique.append(review)

        return unique

    # -----------------------------------------------------

    def _summarize_chunk(
        self,
        reviews: List[Any]
    ) -> Dict[str, Any]:

        prompt = f"""
You are an expert Customer Insight Analyst.

Summarize the following customer reviews.

Goals

- Remove duplicate information.
- Preserve customer intent.
- Identify recurring topics.
- Preserve representative customer quotes.
- Do NOT invent new facts.
- Keep the summary concise.

Customer Reviews

{reviews}

Return ONLY valid JSON.

Required Schema

{{
    "summary": "",

    "key_topics": [

        {{
            "topic": "",
            "mentions": 0
        }}

    ],

    "representative_quotes": [],

    "sentiment_distribution": {{

        "positive": 0,

        "neutral": 0,

        "negative": 0

    }}
}}
"""

        return gemini.generate_json(prompt)

    # -----------------------------------------------------

    def _merge_summaries(
        self,
        summaries: List[Dict[str, Any]]
    ) -> Dict[str, Any]:

        prompt = f"""
You are an expert Customer Insight Analyst.

Merge the following review summaries.

Goals

- Merge similar topics.
- Preserve topic frequencies.
- Preserve representative quotes.
- Produce one master summary.
- Do NOT invent information.

Chunk Summaries

{summaries}

Return ONLY valid JSON.

Schema

{{
    "summary":"",

    "key_topics":[
        {{
            "topic":"",
            "mentions":0
        }}
    ],

    "representative_quotes":[],

    "sentiment_distribution":{{
        "positive":0,
        "neutral":0,
        "negative":0
    }}
}}
"""

        return gemini.generate_json(prompt)

    # -----------------------------------------------------

    @staticmethod
    def _empty_summary():

        return {

            "summary": "",

            "key_topics": [],

            "representative_quotes": [],

            "sentiment_distribution": {
                "positive": 0,
                "neutral": 0,
                "negative": 0
            },

            "statistics": {
                "total_reviews": 0,
                "duplicates_removed": 0,
                "unique_reviews": 0
            }
        }


summarizer = ReviewSummarizer()