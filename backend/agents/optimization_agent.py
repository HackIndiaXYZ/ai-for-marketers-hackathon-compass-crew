"""
Campaign Optimization Agent
===========================

Evaluates generated marketing campaigns and recommends the
best-performing strategy.

Input:
{
    "business_topic": "...",
    "campaigns": [...]
}

Output:
{
    "business_topic": "...",
    "optimized_campaigns": [...]
}
"""

from backend.ai.gemini import gemini
from backend.ai.prompts import optimization_prompt


class OptimizationAgent:

    def __init__(self):
        pass


    def run(self, campaign_output: dict) -> dict:
        """
        Run campaign optimization.
        """


        topic = campaign_output.get(
            "business_topic",
            ""
        )


        campaigns = campaign_output.get(
            "campaigns",
            []
        )


        prompt = optimization_prompt(
            business_topic=topic,
            campaigns=campaigns,
        )


        result = gemini.generate_json(prompt)


        # Debug Gemini response
        print("\n==============================")
        print("OPTIMIZATION GEMINI RESPONSE")
        print("==============================")
        print(result)
        print("==============================\n")


        optimized_campaigns = result.get(
            "optimized_campaigns",
            []
        )


        return {
            "business_topic": topic,
            "optimized_campaigns": optimized_campaigns,
        }