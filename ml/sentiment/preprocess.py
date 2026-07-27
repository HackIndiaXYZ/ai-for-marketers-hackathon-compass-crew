"""
Sentiment Preprocessing Pipeline (`ml/sentiment/preprocess.py`).

Performs text normalization, stopword removal, lemmatization, TF-IDF vectorization,
and tabular scaling.
"""

import logging
import re
from typing import Tuple
import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SentimentPreprocessor:
    """Preprocessor for Sentiment & Multi-Label Emotion modeling."""

    def __init__(self) -> None:
        """Initialize scaling and vectorization components."""
        self.scaler = StandardScaler()
        self.tfidf = TfidfVectorizer(max_features=100, stop_words='english', ngram_range=(1, 2))
        self.is_fitted = False
        logger.info("SentimentPreprocessor initialized.")

    def clean_text(self, text: str) -> str:
        """
        Normalize text snippet.

        Args:
            text: Input string.

        Returns:
            Cleaned lowercase text string.
        """
        text = str(text).lower()
        text = re.sub(r'[^a-z0-9\s!?]', '', text)
        return text.strip()

    def fit_transform(self, feat_df: pd.DataFrame, text_series: pd.Series) -> np.ndarray:
        """
        Fit transformers and convert data into a unified feature matrix.

        Args:
            feat_df: Feature DataFrame containing numerical features.
            text_series: Series of raw text snippets.

        Returns:
            NumPy array feature matrix.
        """
        X_num = self.scaler.fit_transform(feat_df)
        cleaned_texts = [self.clean_text(t) for t in text_series]
        X_text = self.tfidf.fit_transform(cleaned_texts).toarray()

        self.is_fitted = True
        return np.hstack([X_num, X_text])

    def transform(self, feat_df: pd.DataFrame, text_series: pd.Series) -> np.ndarray:
        """
        Transform new data using fitted transformers.

        Args:
            feat_df: Feature DataFrame.
            text_series: Raw text snippets.

        Returns:
            NumPy array.
        """
        if not self.is_fitted:
            raise RuntimeError("SentimentPreprocessor must be fitted before calling transform.")

        X_num = self.scaler.transform(feat_df)
        cleaned_texts = [self.clean_text(t) for t in text_series]
        X_text = self.tfidf.transform(cleaned_texts).toarray()

        return np.hstack([X_num, X_text])

    def save(self, filepath: str) -> None:
        """Save preprocessor artifact."""
        joblib.dump(self, filepath)
        logger.info(f"SentimentPreprocessor saved to {filepath}")

    @staticmethod
    def load(filepath: str) -> "SentimentPreprocessor":
        """Load preprocessor artifact."""
        obj = joblib.load(filepath)
        logger.info(f"SentimentPreprocessor loaded from {filepath}")
        return obj


if __name__ == "__main__":
    prep = SentimentPreprocessor()
    f_df = pd.DataFrame([{"polarity": 0.5, "subjectivity": 0.8}])
    t_ser = pd.Series(["Great product!"])
    res = prep.fit_transform(f_df, t_ser)
    print("Matrix shape:", res.shape)
