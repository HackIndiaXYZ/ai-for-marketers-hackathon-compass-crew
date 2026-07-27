"""
CTR Inference Pipeline (`ml/ctr_prediction/predict.py`).

Provides standalone inference utility and CTRPredictor class for evaluating single/batch ad copy copy text.
"""

import logging
import os
import sys
from typing import Tuple, Optional
import pandas as pd

# Add root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from ml.ctr_prediction.features import CTRFeatureExtractor
from ml.ctr_prediction.model import CTRModel
from ml.ctr_prediction.preprocess import CTRPreprocessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CTRPredictor:
    """Predictor service class loading preprocessor and model for CTR inference."""

    def __init__(self, model_dir: Optional[str] = None) -> None:
        """
        Initialize CTRPredictor with model directory path.

        Args:
            model_dir: Directory containing preprocessor.pkl and model.pkl.
        """
        if model_dir is None:
            model_dir = os.path.dirname(__file__)

        self.model_dir = model_dir
        self.extractor = CTRFeatureExtractor()

        prep_path = os.path.join(self.model_dir, "preprocessor.pkl")
        model_path = os.path.join(self.model_dir, "model.pkl")

        # Load or initialize on the fly if missing
        if os.path.exists(prep_path) and os.path.exists(model_path):
            self.preprocessor = CTRPreprocessor.load(prep_path)
            self.model = CTRModel.load(model_path)
        else:
            logger.info("Artifacts missing. Training on synthetic baseline dataset...")
            from ml.ctr_prediction.train import train_ctr_pipeline
            train_ctr_pipeline(artifact_dir=self.model_dir)
            self.preprocessor = CTRPreprocessor.load(prep_path)
            self.model = CTRModel.load(model_path)

    def predict_single(
        self,
        headline: str,
        body_text: str = "",
        platform: str = "Meta",
        cta: str = "Learn More"
    ) -> Tuple[float, float]:
        """
        Predict CTR percentage for a single ad copy string.

        Args:
            headline: Ad headline.
            body_text: Ad body copy.
            platform: Meta, Google, LinkedIn, etc.
            cta: Call-to-action text.

        Returns:
            Tuple of (predicted_ctr_pct, confidence_score)
        """
        df_raw = pd.DataFrame([{
            "headline": headline,
            "body_text": body_text,
            "platform": platform,
            "cta": cta
        }])

        feat_df = self.extractor.transform_dataframe(df_raw)
        X = self.preprocessor.transform(feat_df, df_raw["headline"])
        predicted_ctr = float(self.model.predict(X)[0])

        confidence = 0.85 if len(headline.split()) >= 4 else 0.65
        return round(predicted_ctr, 2), round(confidence, 2)


if __name__ == "__main__":
    predictor = CTRPredictor()
    ctr, conf = predictor.predict_single(
        headline="Transform Your Sales With AI!",
        body_text="Automate your campaigns today.",
        platform="Meta",
        cta="Get Started Free"
    )
    print(f"Predicted CTR: {ctr}% (Confidence: {conf})")
