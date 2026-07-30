"""
Translator Utility
------------------

Responsibilities
----------------
- Detect review language
- Translate customer reviews to English
- Translate generated marketing campaigns
- Cache repeated translations to reduce Gemini API calls

Supported Languages
-------------------
- English
- Hindi
- Hinglish
- Bengali
"""

from __future__ import annotations

from backend.ai.gemini import gemini


SUPPORTED_LANGUAGES = [
    "English",
    "Hindi",
    "Hinglish",
    "Bengali",
]


class Translator:
    """
    Translation helper used throughout the AI pipeline.

    Workflow

    Raw Reviews
        ↓
    Detect Language
        ↓
    Translate → English
        ↓
    AI Agents
        ↓
    Translate Campaign Output (Optional)
    """

    def __init__(self):
        self.cache = {}

    # ---------------------------------------------------------
    # Internal Cache Helpers
    # ---------------------------------------------------------

    def _get_cache(self, key: str):
        return self.cache.get(key)

    def _set_cache(self, key: str, value: str):
        self.cache[key] = value
        return value

    # ---------------------------------------------------------
    # Detect Language
    # ---------------------------------------------------------

    def detect_language(self, text: str) -> str:
        """
        Detect the language of the supplied text.

        Returns one of:
        - English
        - Hindi
        - Hinglish
        - Bengali
        """

        cache_key = f"detect::{text}"

        cached = self._get_cache(cache_key)
        if cached:
            return cached

        prompt = f"""
You are a language detection expert.

Detect the language of the following text.

Text:
{text}

Choose ONLY one of:

English
Hindi
Hinglish
Bengali

Return ONLY the language name.
"""

        language = gemini.generate(prompt).strip()

        if language not in SUPPORTED_LANGUAGES:
            language = "English"

        return self._set_cache(cache_key, language)

    # ---------------------------------------------------------
    # Translate Review → English
    # ---------------------------------------------------------

    def translate_to_english(self, text: str) -> str:
        """
        Translate customer review into English while preserving
        customer intent and emotional tone.
        """

        cache_key = f"english::{text}"

        cached = self._get_cache(cache_key)
        if cached:
            return cached

        prompt = f"""
You are a professional translator.

Translate the following customer review into English.

Requirements:

- Preserve customer intent.
- Preserve emotional tone.
- Preserve product names.
- Preserve company names.
- Preserve formatting where possible.

Text:

{text}

Return ONLY the translated text.
"""

        translation = gemini.generate(prompt).strip()

        return self._set_cache(cache_key, translation)

    # ---------------------------------------------------------
    # Translate Marketing Content
    # ---------------------------------------------------------

    def translate(
        self,
        text: str,
        target_language: str,
    ) -> str:
        """
        Translate marketing content into the target language.
        """

        if target_language not in SUPPORTED_LANGUAGES:
            raise ValueError(
                f"Unsupported language '{target_language}'. "
                f"Supported languages: {SUPPORTED_LANGUAGES}"
            )

        if target_language == "English":
            return text

        cache_key = f"{target_language}::{text}"

        cached = self._get_cache(cache_key)
        if cached:
            return cached

        prompt = f"""
You are a professional marketing translator.

Translate the following marketing content.

Target Language

{target_language}

Preserve:

- Emotional tone
- Persuasiveness
- Call-to-action
- Formatting
- Brand names
- Product names

Do NOT explain anything.

Return ONLY the translated content.

Content:

{text}
"""

        translation = gemini.generate(prompt).strip()

        return self._set_cache(cache_key, translation)

    # ---------------------------------------------------------
    # Translate Campaign Into All Languages
    # ---------------------------------------------------------

    def translate_campaign(self, text: str) -> dict:
        """
        Translate campaign content into every supported language.
        """

        return {
            "english": text,
            "hindi": self.translate(text, "Hindi"),
            "hinglish": self.translate(text, "Hinglish"),
            "bengali": self.translate(text, "Bengali"),
        }

    # ---------------------------------------------------------
    # Cache Management
    # ---------------------------------------------------------

    def clear_cache(self):
        """Clear translation cache."""
        self.cache.clear()

    def cache_size(self) -> int:
        """Return the number of cached entries."""
        return len(self.cache)


# Singleton instance
translator = Translator()