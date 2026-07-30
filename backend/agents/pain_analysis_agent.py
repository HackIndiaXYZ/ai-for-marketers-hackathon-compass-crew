"""
Pain Analysis Agent

Converts customer reviews into
structured business pain points.
"""

from backend.ai.gemini import gemini
from backend.ai.prompts import pain_analysis_prompt


class PainAnalysisAgent:

    def __init__(self):
        pass

    def run(self, customer_voice_output):
        """
        Analyze cleaned customer reviews
        and return structured pain points.
        """

        # Get processed review data
        processed = customer_voice_output[
            "processed_reviews"
        ]

        # Extract cleaned reviews
        reviews = processed[
            "clean_reviews"
        ]

        # Extract AI-generated summary
        summary = processed[
            "summary"
        ]

        # Get business topic
        topic = customer_voice_output[
            "business_topic"
        ]

        # Build prompt using both reviews and summary
        prompt = pain_analysis_prompt(
            reviews=reviews,
            summary=summary
        )

        # Generate structured pain point analysis
        analysis = gemini.generate_json(prompt)

        return {
            "business_topic": topic,
            "pain_points": analysis.get(
                "pain_points",
                []
            )
        }


pain_analysis_agent = PainAnalysisAgent()