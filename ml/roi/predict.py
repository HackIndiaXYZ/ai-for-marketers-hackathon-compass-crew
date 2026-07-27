"""
ROI Predictor (`ml/roi/predict.py`).

Inference class for predicting expected campaign revenue and ROI multipliers.
"""

import logging
import os
import sys
from typing import Dict, Any, Optional
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from ml.roi.features import ROIFeatureExtractor
from ml.roi.model import ROIPredictionModel
from ml.roi.preprocess import ROIPreprocessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ROIPredictor:
    """Inference service class predicting revenue and ROI multipliers for marketing campaigns."""

    def __init__(self, model_dir: Optional[str] = None) -> None:
        """
        Initialize ROIPredictor.

        Args:
            model_dir: Artifacts directory containing preprocessor.pkl and model.pkl.
        """
        if model_dir is None:
            model_dir = os.path.dirname(__file__)

        self.model_dir = model_dir
        self.extractor = ROIFeatureExtractor()

        prep_path = os.path.join(self.model_dir, "preprocessor.pkl")
        model_path = os.path.join(self.model_dir, "model.pkl")

        if os.path.exists(prep_path) and os.path.exists(model_path):
            self.preprocessor = ROIPreprocessor.load(prep_path)
            self.model = ROIPredictionModel.load(model_path)
        else:
            logger.info("ROI artifacts missing. Training synthetic ROI model...")
            from ml.roi.train import train_roi_pipeline
            train_roi_pipeline(artifact_dir=self.model_dir)
            self.preprocessor = ROIPreprocessor.load(prep_path)
            self.model = ROIPredictionModel.load(model_path)

    def predict_campaign_roi(
        self,
        budget: float,
        impressions: float,
        predicted_ctr_pct: float,
        conversion_rate_pct: float = 2.5,
        average_order_value: float = 120.0,
        channel: str = "Meta Ads"
    ) -> Dict[str, Any]:
        """
        Predict campaign gross revenue, net profit, and ROI ratio.

        Args:
            budget: Campaign budget USD.
            impressions: Target impressions reach.
            predicted_ctr_pct: Predicted CTR %.
            conversion_rate_pct: Landing page conversion rate %.
            average_order_value: Order value in USD.
            channel: Marketing channel string.

        Returns:
            Dictionary containing predicted revenue, profit, ROI multiplier, and confidence.
        """
        df_raw = pd.DataFrame([{
            "budget": budget,
            "impressions": impressions,
            "predicted_ctr_pct": predicted_ctr_pct,
            "conversion_rate_pct": conversion_rate_pct,
            "average_order_value": average_order_value,
            "channel": channel
        }])

        feat_df = self.extractor.transform_dataframe(df_raw)
        X = self.preprocessor.transform(feat_df)

        predicted_revenue = float(self.model.predict(X)[0])
        net_profit = predicted_revenue - budget
        roi_multiplier = round(predicted_revenue / max(budget, 1.0), 2)

        return {
            "budget": budget,
            "channel": channel,
            "predicted_revenue": round(predicted_revenue, 2),
            "predicted_net_profit": round(net_profit, 2),
            "roi_multiplier": roi_multiplier,
            "roi_percentage": round((net_profit / max(budget, 1.0)) * 100.0, 2)
        }


if __name__ == "__main__":
    predictor = ROIPredictor()
    result = predictor.predict_campaign_roi(
        budget=5000.0,
        impressions=250000.0,
        predicted_ctr_pct=2.2,
        conversion_rate_pct=3.0,
        average_order_value=150.0,
        channel="Meta Ads"
    )
    print("ROI Prediction Result:", result)
