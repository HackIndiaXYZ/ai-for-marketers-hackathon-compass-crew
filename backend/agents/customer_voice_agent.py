from typing import List, Dict

from backend.ai.prompts import customer_voice_prompt
from backend.ai.gemini import gemini
from backend.ai.summarizer import summarizer


class CustomerVoiceAgent:

    def remove_empty(self, reviews: List[Dict]) -> List[Dict]:
        """
        Remove reviews with empty or missing text.
        """

        return [
            review
            for review in reviews
            if review.get("text")
            and review["text"].strip()
        ]


    def remove_duplicates(self, reviews: List[Dict]) -> List[Dict]:
        """
        Remove duplicate reviews based on review text.
        """

        seen = set()
        unique_reviews = []

        for review in reviews:
            text = review.get("text", "").strip().lower()

            if text not in seen:
                seen.add(text)
                unique_reviews.append(review)

        return unique_reviews


    def normalize(self, reviews: List[Dict]) -> List[Dict]:
        """
        Normalize review structure before sending to Gemini.
        """

        normalized_reviews = []

        for review in reviews:
            normalized_reviews.append(
                {
                    "source": review.get(
                        "source",
                        "unknown"
                    ),
                    "text": review.get(
                        "text",
                        ""
                    ).strip()
                }
            )

        return normalized_reviews


    def run(
        self,
        topic: str,
        reviews: List[Dict]
    ) -> Dict:
        """
        Execute Customer Voice pipeline.
        """

        print("\n" + "=" * 60)
        print("Starting Customer Voice Agent")
        print("=" * 60)

        # ---------------------------------------------------------
        # Step 1: Remove empty reviews
        # ---------------------------------------------------------

        reviews = self.remove_empty(reviews)

        print(f"Reviews after removing empty: {len(reviews)}")

        # ---------------------------------------------------------
        # Step 2: Remove duplicate reviews
        # ---------------------------------------------------------

        reviews = self.remove_duplicates(reviews)

        print(f"Reviews after removing duplicates: {len(reviews)}")

        if not reviews:
            raise RuntimeError(
                "No valid reviews available after preprocessing."
            )

        # ---------------------------------------------------------
        # Step 3: Normalize reviews
        # ---------------------------------------------------------

        normalized_reviews = self.normalize(reviews)

        print(f"Normalized reviews: {len(normalized_reviews)}")

        # ---------------------------------------------------------
        # Reduce size during testing
        # ---------------------------------------------------------

        normalized_reviews = normalized_reviews[:10]

        # ---------------------------------------------------------
        # Step 4: Generate Prompt
        # ---------------------------------------------------------

        prompt = customer_voice_prompt(
            normalized_reviews
        )

        print("Sending request to Gemini...")

        # ---------------------------------------------------------
        # Step 5: Gemini Cleaning
        # ---------------------------------------------------------

        cleaned = gemini.generate_json(prompt)

        if not isinstance(cleaned, dict):
            raise RuntimeError(
                "Gemini returned an invalid response."
            )

        if cleaned.get("success") is False:
            raise RuntimeError(
                cleaned.get(
                    "error",
                    "Unknown Gemini error."
                )
            )

        clean_reviews = cleaned.get("clean_reviews")

        if clean_reviews is None:
            raise RuntimeError(
                "Gemini response does not contain 'clean_reviews'."
            )

        if not isinstance(clean_reviews, list):
            raise RuntimeError(
                "'clean_reviews' should be a list."
            )

        print(
            f"Gemini returned {len(clean_reviews)} cleaned reviews."
        )

        # ---------------------------------------------------------
        # Step 6: Generate Summary
        # ---------------------------------------------------------

        review_summary = summarizer.summarize_reviews(
            clean_reviews
        )

        print(
            "Customer Voice Agent completed successfully."
        )

        return {
            "business_topic": topic,

            "processed_reviews": {
                "clean_reviews": clean_reviews,
                "summary": review_summary
            }
        }