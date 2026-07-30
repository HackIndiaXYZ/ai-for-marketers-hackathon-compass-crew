"""
Persona Intelligence Agent
--------------------------

Converts business pain points into
high-value customer personas.

Responsibilities:
- Receive structured pain points
- Generate customer personas
- Return personas for Campaign Agent
"""

from backend.ai.gemini import gemini
from backend.ai.prompts import persona_prompt


class PersonaAgent:

    def __init__(self):
        pass

    def run(self, pain_analysis_output):
        """
        Generate customer personas from
        structured pain point analysis.
        """

        topic = pain_analysis_output["business_topic"]

        pain_points = pain_analysis_output["pain_points"]

        prompt = persona_prompt(pain_points)

        personas = gemini.generate_json(prompt)

        return {
            "business_topic": topic,
            "personas": personas.get(
                "personas",
                []
            )
        }