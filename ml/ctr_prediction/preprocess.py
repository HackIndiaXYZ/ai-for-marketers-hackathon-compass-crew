"""
CTR Preprocessing Pipeline (`ml/ctr_prediction/preprocess.py`).

Scales numerical features, encodes categorical variables, and vectorizes ad text.
"""

import logging
from typing import Tuple, Any
import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CTRPreprocessor:
    """Preprocessor handling TF-IDF vectorization and tabular scaling."""

    def __init__(self) -> None:
        """Initialize transformer components."""
        self.scaler = StandardScaler()
        self.encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
        self.tfidf = TfidfVectorizer(max_features=50, stop_words='english')
        self.is_fitted = False
        logger.info("CTRPreprocessor initialized.")

    def fit_transform(self, df: pd.DataFrame, headlines: pd.Series) -> np.ndarray:
        """
        Fit preprocessor and transform features into a unified matrix.

        Args:
            df: DataFrame containing numerical and categorical columns.
            headlines: Series of headline text strings.

        Returns:
            Concatenated NumPy feature matrix.
        """
        num_cols = ["word_count", "char_count", "power_word_count", "has_question", "has_exclamation", "uppercase_ratio"]
        cat_cols = ["platform", "cta"]

        X_num = self.scaler.fit_transform(df[num_cols])
        X_cat = self.encoder.fit_transform(df[cat_cols])
        X_text = self.tfidf.fit_transform(headlines.fillna("")).toarray()

        self.is_fitted = True
        return np.hstack([X_num, X_cat, X_text])

    def transform(self, df: pd.DataFrame, headlines: pd.Series) -> np.ndarray:
        """
        Transform new data using fitted transformers.

        Args:
            df: DataFrame of features.
            headlines: Series of headlines.

        Returns:
            NumPy feature matrix.
        """
        if not self.is_fitted:
            raise RuntimeError("CTRPreprocessor must be fitted before calling transform.")

        num_cols = ["word_count", "char_count", "power_word_count", "has_question", "has_exclamation", "uppercase_ratio"]
        cat_cols = ["platform", "cta"]

        X_num = self.scaler.transform(df[num_cols])
        X_cat = self.encoder.transform(df[cat_cols])
        X_text = self.tfidf.transform(headlines.fillna("")).toarray()

        return np.hstack([X_num, X_cat, X_text])

    def save(self, filepath: str) -> None:
        """Save preprocessor artifact."""
        joblib.dump(self, filepath)
        logger.info(f"Saved preprocessor to {filepath}")

    @staticmethod
    def load(filepath: str) -> "CTRPreprocessor":
        """Load preprocessor artifact."""
        obj = joblib.load(filepath)
        logger.info(f"Loaded preprocessor from {filepath}")
        return obj


if __name__ == "__main__":
    prep = CTRPreprocessor()
    df = pd.DataFrame([{
        "word_count": 5.0, "char_count": 30.0, "power_word_count": 1.0,
        "has_question": 0.0, "has_exclamation": 1.0, "uppercase_ratio": 0.1,
        "platform": "Meta", "cta": "Learn More"
    }])
    headlines = pd.Series(["Boost Your Sales Instantly!"])
    matrix = prep.fit_transform(df, headlines)
    print("Preprocessed Matrix Shape:", matrix.shape)
