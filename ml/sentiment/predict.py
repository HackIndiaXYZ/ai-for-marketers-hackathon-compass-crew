"""
Sentiment & Emotion Predictor (`ml/sentiment/predict.py`).

Inference class and standalone entrypoint for sentiment polarity and multi-label emotion prediction.
"""

import logging
import os
import sys
from typing import Dict, List, Any, Optional
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from ml.sentiment.features import SentimentFeatureExtractor
from ml.sentiment.model import SentimentEmotionModel
from ml.sentiment.preprocess import SentimentPreprocessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SentimentPredictor:
    """Predictor wrapper for sentiment polarity and multi-label emotion tagging."""

    EMOTIONS = ["joy", "anger", "sadness", "fear", "frustration"]

    def __init__(self, model_dir: Optional[str] = None) -> None:
        """
        Initialize SentimentPredictor.

        Args:
            model_dir: Artifacts directory containing preprocessor.pkl and model.pkl.
        """
        if model_dir is None:
            model_dir = os.path.dirname(__file__)

        self.model_dir = model_dir
        self.extractor = SentimentFeatureExtractor()

        prep_path = os.path.join(self.model_dir, "preprocessor.pkl")
        model_path = os.path.join(self.model_dir, "model.pkl")

        if os.path.exists(prep_path) and os.path.exists(model_path):
            self.preprocessor = SentimentPreprocessor.load(prep_path)
            self.model = SentimentEmotionModel.load(model_path)
        else:
            logger.info("Sentiment artifacts missing. Training synthetic model...")
            from ml.sentiment.train import train_sentiment_pipeline
            train_sentiment_pipeline(artifact_dir=self.model_dir)
            self.preprocessor = SentimentPreprocessor.load(prep_path)
            self.model = SentimentEmotionModel.load(model_path)

    def predict_text(self, text: str) -> Dict[str, Any]:
        """
        Predict sentiment polarity and multi-label emotions for a raw text string.

        Args:
            text: Input customer feedback string.

        Returns:
            Dictionary containing sentiment polarity, sentiment label, and detected emotions.
        """
        df_raw = pd.DataFrame([{"text": text}])
        feat_df = self.extractor.transform_dataframe(df_raw, text_column="text")
        X = self.preprocessor.transform(feat_df, df_raw["text"])

        emo_matrix, pol_array = self.model.predict(X)
        emo_binary = emo_matrix[0]
        polarity = float(pol_array[0])

        detected = [self.EMOTIONS[i] for i, flag in enumerate(emo_binary) if flag == 1]
        sentiment_label = "Positive" if polarity > 0.15 else ("Negative" if polarity < -0.15 else "Neutral")

        return {
            "text": text,
            "sentiment": sentiment_label,
            "polarity_score": round(polarity, 3),
            "detected_emotions": detected
        }


if __name__ == "__main__":
    predictor = SentimentPredictor()
    result = predictor.predict_text("I am very frustrated because the system keeps lagging!")
    print("Inference Result:", result)
