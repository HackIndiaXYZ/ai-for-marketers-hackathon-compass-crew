"""
Sentiment & Multi-Label Emotion Model (`ml/sentiment/model.py`).

Provides multi-label emotion classification and continuous sentiment polarity prediction.
"""

import logging
from typing import Dict, List, Tuple
import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.multioutput import MultiOutputClassifier

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SentimentEmotionModel:
    """Multi-Label Emotion Classifier and Sentiment Polarity Regressor."""

    EMOTIONS = ["joy", "anger", "sadness", "fear", "frustration"]

    def __init__(self) -> None:
        """Initialize multi-label classifier and polarity regressor."""
        base_lr = LogisticRegression(class_weight='balanced', max_iter=200, random_state=42)
        self.emotion_classifier = MultiOutputClassifier(base_lr)
        self.polarity_regressor = Ridge(alpha=1.0)
        self.is_trained = False
        logger.info("SentimentEmotionModel initialized.")

    def fit(self, X: np.ndarray, y_emotions: np.ndarray, y_polarity: np.ndarray) -> "SentimentEmotionModel":
        """
        Fit multi-label emotion classifier and sentiment polarity regressor.

        Args:
            X: Feature matrix.
            y_emotions: Binary multi-label array of shape (N, 5).
            y_polarity: Polarity target array of shape (N,).

        Returns:
            Fitted model instance.
        """
        logger.info("Fitting SentimentEmotionModel on dataset...")
        self.emotion_classifier.fit(X, y_emotions)
        self.polarity_regressor.fit(X, y_polarity)
        self.is_trained = True
        return self

    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Predict binary multi-label emotions and polarity scores.

        Args:
            X: Feature matrix.

        Returns:
            Tuple of (emotion_labels_matrix, predicted_polarities_array)
        """
        if not self.is_trained:
            raise RuntimeError("SentimentEmotionModel must be trained before predict.")

        emotion_preds = self.emotion_classifier.predict(X)
        polarity_preds = self.polarity_regressor.predict(X)
        polarity_preds = np.clip(polarity_preds, -1.0, 1.0)

        return emotion_preds, polarity_preds

    def save(self, filepath: str) -> None:
        """Save model artifact."""
        joblib.dump(self, filepath)
        logger.info(f"Saved SentimentEmotionModel to {filepath}")

    @staticmethod
    def load(filepath: str) -> "SentimentEmotionModel":
        """Load model artifact."""
        obj = joblib.load(filepath)
        logger.info(f"Loaded SentimentEmotionModel from {filepath}")
        return obj


if __name__ == "__main__":
    X_dummy = np.random.randn(40, 15)
    y_emo = np.random.randint(0, 2, size=(40, 5))
    y_pol = np.random.uniform(-1.0, 1.0, 40)

    m = SentimentEmotionModel()
    m.fit(X_dummy, y_emo, y_pol)
    e_p, p_p = m.predict(X_dummy[:3])
    print("Emotions:\n", e_p)
    print("Polarities:\n", p_p)
