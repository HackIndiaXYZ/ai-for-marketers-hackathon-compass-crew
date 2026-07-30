"""
Campaign Generation Agent
-------------------------

Generates personalized multi-channel
marketing campaigns from customer personas.
"""

from backend.ai.gemini import gemini
from backend.ai.prompts import campaign_prompt


class CampaignAgent:

    def __init__(self):
        pass

    def run(self, persona_output):
        """
        Generate complete marketing campaigns
        for each customer persona.
        """

        topic = persona_output["business_topic"]

        personas = persona_output["personas"]

        prompt = campaign_prompt(
            business_topic=topic,
            personas=personas,
        )

        campaigns = gemini.generate_json(prompt)

        return {
            "business_topic": topic,
            "campaigns": campaigns.get(
                "campaigns",
                []
            )
        }