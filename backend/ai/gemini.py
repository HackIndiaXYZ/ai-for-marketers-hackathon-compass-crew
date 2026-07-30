"""
Gemini Client
-------------
Centralized wrapper around the Gemini API.

Responsibilities
----------------
- Initialize Gemini once
- Handle API communication
- Return plain text responses
- Return structured JSON responses
- Hide Gemini SDK details from other modules
"""

import json
import os
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentConfig

# ------------------------------------------------------------------
# Load backend/.env explicitly
# ------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_FILE)

# Uncomment these lines for debugging if needed
# print("Loading .env from:", ENV_FILE)
# print("GEMINI_API_KEY =", os.getenv("GEMINI_API_KEY"))


class GeminiClient:
    """
    Reusable Gemini Client.

    Example
    -------
    from backend.ai.gemini import gemini

    response = gemini.generate("Hello")
    """

    def __init__(self) -> None:
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                f"GEMINI_API_KEY not found.\n"
                f"Expected .env at: {ENV_FILE}"
            )

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash",
        )

        self.client = genai.Client(api_key=api_key)

    def generate(
        self,
        prompt: str,
        temperature: float = 0.3,
    ) -> str:
        """
        Generate plain text using Gemini.
        """

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=GenerateContentConfig(
                    temperature=temperature,
                ),
            )

            return (response.text or "").strip()

        except Exception as e:
            raise RuntimeError(
                f"Gemini API Error: {e}"
            ) from e

    def generate_json(
        self,
        prompt: str,
        temperature: float = 0.2,
    ) -> Dict[str, Any]:
        """
        Generate structured JSON.

        IMPORTANT:
        The prompt should instruct Gemini to ONLY return JSON.
        """

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=GenerateContentConfig(
                    temperature=temperature,
                    response_mime_type="application/json",
                ),
            )

            text = (response.text or "").strip()

            # Remove markdown fences if Gemini accidentally returns them
            text = (
                text.replace("```json", "")
                .replace("```", "")
                .strip()
            )

            return json.loads(text)

        except json.JSONDecodeError:
            return {
                "success": False,
                "error": "Invalid JSON returned by Gemini.",
                "raw_response": text if "text" in locals() else "",
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }


# Singleton instance
gemini = GeminiClient()