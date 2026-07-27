"""
Persona Preprocessing Pipeline (`ml/persona/preprocess.py`).

Standardizes features, performs PCA/TruncatedSVD dimensionality reduction, and vectorizes text.
"""

import logging
import joblib
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PersonaPreprocessor:
    """Preprocessor for Customer Persona clustering."""

    def __init__(self, n_components: int = 5) -> None:
        """
        Initialize transformers.

        Args:
            n_components: Number of PCA components.
        """
        self.scaler = StandardScaler()
        self.tfidf = TfidfVectorizer(max_features=50, stop_words='english')
        self.pca = PCA(n_components=n_components, random_state=42)
        self.is_fitted = False
        logger.info("PersonaPreprocessor initialized.")

    def fit_transform(self, feat_df: pd.DataFrame, text_series: pd.Series) -> np.ndarray:
        """
        Fit transformers and reduce dimensionality for clustering.

        Args:
            feat_df: Feature DataFrame.
            text_series: Series of text strings.

        Returns:
            Reduced feature matrix.
        """
        X_num = self.scaler.fit_transform(feat_df)
        X_text = self.tfidf.fit_transform(text_series.fillna("")).toarray()

        combined = np.hstack([X_num, X_text])
        n_comp = min(self.pca.n_components, combined.shape[1], combined.shape[0] - 1)
        if n_comp < self.pca.n_components:
            self.pca = PCA(n_components=max(n_comp, 1), random_state=42)

        reduced = self.pca.fit_transform(combined)
        self.is_fitted = True
        return reduced

    def transform(self, feat_df: pd.DataFrame, text_series: pd.Series) -> np.ndarray:
        """
        Transform new data using fitted models.

        Args:
            feat_df: Feature DataFrame.
            text_series: Series of text snippets.

        Returns:
            Reduced feature array.
        """
        if not self.is_fitted:
            raise RuntimeError("PersonaPreprocessor must be fitted before transform.")

        X_num = self.scaler.transform(feat_df)
        X_text = self.tfidf.transform(text_series.fillna("")).toarray()
        combined = np.hstack([X_num, X_text])
        return self.pca.transform(combined)

    def save(self, filepath: str) -> None:
        """Save preprocessor artifact."""
        joblib.dump(self, filepath)
        logger.info(f"Saved PersonaPreprocessor to {filepath}")

    @staticmethod
    def load(filepath: str) -> "PersonaPreprocessor":
        """Load preprocessor artifact."""
        obj = joblib.load(filepath)
        logger.info(f"Loaded PersonaPreprocessor from {filepath}")
        return obj


if __name__ == "__main__":
    prep = PersonaPreprocessor(n_components=3)
    f_df = pd.DataFrame([{"text_length": 50.0, "polarity": 0.2}])
    t_ser = pd.Series(["Great API integration"])
    m = prep.fit_transform(f_df, t_ser)
    print("Preprocessed shape:", m.shape)
