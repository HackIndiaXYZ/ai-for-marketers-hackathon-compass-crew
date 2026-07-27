"""
CTR Feature Extraction Module (`ml/ctr_prediction/features.py`).

Extracts numerical, categorical, and text-based feature arrays for Click-Through-Rate (CTR) ML modeling.
"""

import logging
import re
from typing import Dict, List, Any
import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CTRFeatureExtractor:
    """Feature extractor for ad copy text, platform encodings, and targeting signals."""

    POWER_WORDS = {"free", "instant", "guaranteed", "proven", "unlock", "boost", "exclusive", "now", "save"}

    def __init__(self) -> None:
        """Initialize extractor."""
        logger.info("CTRFeatureExtractor initialized.")

    def extract_text_features(self, headline: str, body_text: str = "") -> Dict[str, float]:
        """
        Extract numerical features from headline and body copy.

        Args:
            headline: Headline string.
            body_text: Body text string.

        Returns:
            Dictionary of numerical feature values.
        """
        text = f"{headline} {body_text}".strip()
        words = text.split()
        word_count = len(words)
        char_count = len(text)

        power_word_count = sum(1 for w in words if w.lower().strip("!?,.") in self.POWER_WORDS)
        has_question = 1.0 if "?" in headline else 0.0
        has_exclamation = 1.0 if "!" in text else 0.0
        uppercase_ratio = sum(1 for c in text if c.isupper()) / max(char_count, 1)

        return {
            "word_count": float(word_count),
            "char_count": float(char_count),
            "power_word_count": float(power_word_count),
            "has_question": has_question,
            "has_exclamation": has_exclamation,
            "uppercase_ratio": float(round(uppercase_ratio, 4))
        }

    def transform_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform a raw DataFrame of ad records into feature engineering DataFrame.

        Args:
            df: Raw DataFrame containing 'headline', 'body_text', 'platform', 'cta'.

        Returns:
            Feature DataFrame.
        """
        if df.empty:
            return pd.DataFrame()

        records = []
        for idx, row in df.iterrows():
            feat = self.extract_text_features(
                headline=str(row.get("headline", "")),
                body_text=str(row.get("body_text", ""))
            )
            feat["platform"] = str(row.get("platform", "Meta"))
            feat["cta"] = str(row.get("cta", "Learn More"))
            records.append(feat)

        return pd.DataFrame(records)


if __name__ == "__main__":
    extractor = CTRFeatureExtractor()
    sample_df = pd.DataFrame([{
        "headline": "Boost Your Sales Instantly!",
        "body_text": "Join thousands of marketers today.",
        "platform": "Meta",
        "cta": "Sign Up"
    }])
    print(extractor.transform_dataframe(sample_df))
