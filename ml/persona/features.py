"""
Persona Feature Extraction Module (`ml/persona/features.py`).

Transforms raw customer feedback text and behavioral metrics into feature vectors for clustering.
"""

import logging
from typing import Dict, List
import pandas as pd
from textblob import TextBlob

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PersonaFeatureExtractor:
    """Feature Extractor for Persona Clustering ML pipeline."""

    ROLE_KEYWORDS = ["code", "api", "price", "ui", "ux", "marketing", "ads", "speed", "support"]

    def __init__(self) -> None:
        """Initialize Feature Extractor."""
        logger.info("PersonaFeatureExtractor initialized.")

    def extract_features(self, text: str, user_activity_score: float = 1.0) -> Dict[str, float]:
        """
        Extract numerical features from single feedback sample.

        Args:
            text: Customer text string.
            user_activity_score: Numeric score representing user activity level.

        Returns:
            Dictionary of numerical features.
        """
        text_lower = text.lower()
        blob = TextBlob(text)

        feats = {
            "text_length": float(len(text)),
            "word_count": float(len(text.split())),
            "polarity": float(blob.sentiment.polarity),
            "subjectivity": float(blob.sentiment.subjectivity),
            "user_activity_score": float(user_activity_score)
        }

        for kw in self.ROLE_KEYWORDS:
            feats[f"has_kw_{kw}"] = 1.0 if kw in text_lower else 0.0

        return feats

    def transform_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform DataFrame containing 'text' and optional 'activity_score' into feature matrix.

        Args:
            df: Input DataFrame.

        Returns:
            Feature DataFrame.
        """
        records = []
        for idx, row in df.iterrows():
            text = str(row.get("text", ""))
            activity = float(row.get("activity_score", 1.0))
            records.append(self.extract_features(text, activity))

        return pd.DataFrame(records)


if __name__ == "__main__":
    extractor = PersonaFeatureExtractor()
    sample_df = pd.DataFrame([{"text": "API response latency is slow for python developers"}])
    print(extractor.transform_dataframe(sample_df))
