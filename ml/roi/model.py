"""
ROI Prediction Model (`ml/roi/model.py`).

RandomForest & Gradient Boosting ensemble regressor predicting gross revenue and net ROI multiplier.
"""

import logging
import joblib
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ROIPredictionModel:
    """Ensemble Regressor model predicting revenue and ROI multiplier."""

    def __init__(self, n_estimators: int = 100) -> None:
        """
        Initialize ROIPredictionModel.

        Args:
            n_estimators: Number of trees.
        """
        self.rf_model = RandomForestRegressor(n_estimators=n_estimators, random_state=42)
        self.gb_model = GradientBoostingRegressor(n_estimators=n_estimators, random_state=42)
        self.is_trained = False
        logger.info("ROIPredictionModel initialized.")

    def fit(self, X: np.ndarray, y_revenue: np.ndarray) -> "ROIPredictionModel":
        """
        Fit models on campaign features and revenue targets.

        Args:
            X: Feature matrix.
            y_revenue: Target gross revenue.

        Returns:
            Fitted model instance.
        """
        logger.info(f"Fitting ROIPredictionModel on {X.shape[0]} campaign samples...")
        self.rf_model.fit(X, y_revenue)
        self.gb_model.fit(X, y_revenue)
        self.is_trained = True
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict blended gross revenue.

        Args:
            X: Feature matrix.

        Returns:
            Array of predicted gross revenues.
        """
        if not self.is_trained:
            raise RuntimeError("ROIPredictionModel must be trained before predict.")

        rf_preds = self.rf_model.predict(X)
        gb_preds = self.gb_model.predict(X)

        blended = (0.5 * rf_preds) + (0.5 * gb_preds)
        return np.maximum(blended, 0.0)

    def save(self, filepath: str) -> None:
        """Save model artifact."""
        joblib.dump(self, filepath)
        logger.info(f"Saved ROIPredictionModel to {filepath}")

    @staticmethod
    def load(filepath: str) -> "ROIPredictionModel":
        """Load model artifact."""
        obj = joblib.load(filepath)
        logger.info(f"Loaded ROIPredictionModel from {filepath}")
        return obj


if __name__ == "__main__":
    X_dummy = np.random.randn(30, 10)
    y_dummy = np.random.uniform(2000.0, 15000.0, 30)

    m = ROIPredictionModel()
    m.fit(X_dummy, y_dummy)
    preds = m.predict(X_dummy[:3])
    print("Predicted Revenues:", preds)
