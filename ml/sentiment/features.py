"""
Sentiment & Emotion Feature Extractor (`ml/sentiment/features.py`).

Extracts sentiment lexicons (TextBlob/NLTK VADER style), punctuation triggers,
and text embedding representations.
"""

import logging
import re
from typing import Dict, List
import numpy as np
import pandas as pd
from textblob import TextBlob

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SentimentFeatureExtractor:
    """Feature Extractor for Sentiment and Multi-Label Emotion Classifiers."""

    EMOTION_KEYWORDS = {
        "joy": ["love", "happy", "great", "excellent", "awesome", "fantastic", "amazing"],
        "anger": ["hate", "furious", "mad", "disgusted", "annoyed", "terrible", "outraged"],
        "sadness": ["sad", "disappointed", "depressing", "regret", "upset", "sorry"],
        "fear": ["scared", "afraid", "worried", "anxious", "risk", "terrified"],
        "frustration": ["frustrating", "stuck", "broken", "painful", "useless", "clunky"]
    }

    def __init__(self) -> None:
        """Initialize Feature Extractor."""
        logger.info("SentimentFeatureExtractor initialized.")

    def extract_lexicon_features(self, text: str) -> Dict[str, float]:
        """
        Extract numerical features including polarity, subjectivity, and emotion keyword density.

        Args:
            text: Input string.

        Returns:
            Dictionary of feature values.
        """
        text_clean = text.lower()
        blob = TextBlob(text)

        polarity = float(blob.sentiment.polarity)
        subjectivity = float(blob.sentiment.subjectivity)

        feats = {
            "polarity": polarity,
            "subjectivity": subjectivity,
            "text_length": float(len(text)),
            "word_count": float(len(text.split())),
            "exclamation_count": float(text.count("!")),
            "uppercase_count": float(sum(1 for w in text.split() if w.isupper() and len(w) > 1))
        }

        # Add keyword counts per emotion label
        for emotion, kw_list in self.EMOTION_KEYWORDS.items():
            count = sum(1 for kw in kw_list if kw in text_clean)
            feats[f"kw_density_{emotion}"] = float(count)

        return feats

    def transform_dataframe(self, df: pd.DataFrame, text_column: str = "text") -> pd.DataFrame:
        """
        Transform a Series/DataFrame of text snippets into feature DataFrame.

        Args:
            df: Input DataFrame.
            text_column: Column name containing text.

        Returns:
            Feature DataFrame.
        """
        records = []
        for text in df[text_column].fillna(""):
            records.append(self.extract_lexicon_features(str(text)))

        return pd.DataFrame(records)


if __name__ == "__main__":
    extractor = SentimentFeatureExtractor()
    sample_df = pd.DataFrame([{"text": "I absolutely love this amazing product!"}])
    print(extractor.transform_dataframe(sample_df))
