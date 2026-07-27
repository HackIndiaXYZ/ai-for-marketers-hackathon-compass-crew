"""
CTR Model Architecture (`ml/ctr_prediction/model.py`).

Gradient Boosting Regressor ensemble wrapper for CTR estimation.
"""

import logging
from typing import Tuple
import joblib
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CTRModel:
    """Ensemble Regression model predicting ad copy CTR percentage."""

    def __init__(self, n_estimators: int = 100, learning_rate: float = 0.05) -> None:
        """
        Initialize CTRModel.

        Args:
            n_estimators: Trees count.
            learning_rate: Gradient boosting learning rate.
        """
        self.gb_model = GradientBoostingRegressor(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            random_state=42
        )
        self.rf_model = RandomForestRegressor(
            n_estimators=50,
            random_state=42
        )
        self.is_trained = False
        logger.info("CTRModel initialized.")

    def fit(self, X: np.ndarray, y: np.ndarray) -> "CTRModel":
        """
        Fit ensemble regression models.

        Args:
            X: Feature matrix.
            y: Target CTR array.

        Returns:
            Fitted CTRModel instance.
        """
        logger.info(f"Fitting CTRModel ensemble on {X.shape[0]} samples...")
        self.gb_model.fit(X, y)
        self.rf_model.fit(X, y)
        self.is_trained = True
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict blended ensemble CTR percentage.

        Args:
            X: Feature matrix.

        Returns:
            Predicted CTR array.
        """
        if not self.is_trained:
            raise RuntimeError("Model must be trained before calling predict.")

        gb_preds = self.gb_model.predict(X)
        rf_preds = self.rf_model.predict(X)
        blended = (0.6 * gb_preds) + (0.4 * rf_preds)
        return np.clip(blended, 0.05, 20.0)

    def save(self, filepath: str) -> None:
        """Save trained model."""
        joblib.dump(self, filepath)
        logger.info(f"CTRModel saved to {filepath}")

    @staticmethod
    def load(filepath: str) -> "CTRModel":
        """Load saved model."""
        model = joblib.load(filepath)
        logger.info(f"CTRModel loaded from {filepath}")
        return model


if __name__ == "__main__":
    X_dummy = np.random.randn(50, 10)
    y_dummy = np.random.uniform(0.5, 4.0, 50)
    model = CTRModel()
    model.fit(X_dummy, y_dummy)
    preds = model.predict(X_dummy[:5])
    print("Predictions:", preds)
