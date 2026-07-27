"""
ROI Preprocessing Pipeline (`ml/roi/preprocess.py`).

Scales numerical metrics and encodes marketing channel categoricals.
"""

import logging
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ROIPreprocessor:
    """Preprocessor scaling marketing numerical attributes and encoding channels."""

    NUM_COLS = [
        "budget", "log_budget", "impressions", "log_impressions",
        "predicted_ctr_pct", "conversion_rate_pct", "average_order_value",
        "expected_clicks", "expected_conversions"
    ]
    CAT_COLS = ["channel"]

    def __init__(self) -> None:
        """Initialize transformers."""
        self.scaler = StandardScaler()
        self.encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
        self.is_fitted = False
        logger.info("ROIPreprocessor initialized.")

    def fit_transform(self, feat_df: pd.DataFrame) -> np.ndarray:
        """
        Fit preprocessors and return unified numpy feature array.

        Args:
            feat_df: Feature DataFrame.

        Returns:
            Concatenated NumPy array.
        """
        X_num = self.scaler.fit_transform(feat_df[self.NUM_COLS])
        X_cat = self.encoder.fit_transform(feat_df[self.CAT_COLS])

        self.is_fitted = True
        return np.hstack([X_num, X_cat])

    def transform(self, feat_df: pd.DataFrame) -> np.ndarray:
        """
        Transform new DataFrame using fitted preprocessors.

        Args:
            feat_df: Feature DataFrame.

        Returns:
            NumPy feature array.
        """
        if not self.is_fitted:
            raise RuntimeError("ROIPreprocessor must be fitted before transform.")

        X_num = self.scaler.transform(feat_df[self.NUM_COLS])
        X_cat = self.encoder.transform(feat_df[self.CAT_COLS])

        return np.hstack([X_num, X_cat])

    def save(self, filepath: str) -> None:
        """Save preprocessor artifact."""
        joblib.dump(self, filepath)
        logger.info(f"Saved ROIPreprocessor to {filepath}")

    @staticmethod
    def load(filepath: str) -> "ROIPreprocessor":
        """Load preprocessor artifact."""
        obj = joblib.load(filepath)
        logger.info(f"Loaded ROIPreprocessor from {filepath}")
        return obj


if __name__ == "__main__":
    prep = ROIPreprocessor()
    f_df = pd.DataFrame([{
        "budget": 1000.0, "log_budget": 6.9, "impressions": 50000.0, "log_impressions": 10.8,
        "predicted_ctr_pct": 2.0, "conversion_rate_pct": 2.5, "average_order_value": 100.0,
        "expected_clicks": 1000.0, "expected_conversions": 25.0, "channel": "Meta Ads"
    }])
    matrix = prep.fit_transform(f_df)
    print("Matrix shape:", matrix.shape)
