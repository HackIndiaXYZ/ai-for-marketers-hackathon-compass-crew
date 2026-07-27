"""
ROI Feature Extractor (`ml/roi/features.py`).

Extracts numerical marketing features, spend levels, CTR predictions, and log scaling metrics.
"""

import logging
from typing import Dict
import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ROIFeatureExtractor:
    """Feature Extractor for marketing ROI forecasting."""

    def __init__(self) -> None:
        """Initialize Feature Extractor."""
        logger.info("ROIFeatureExtractor initialized.")

    def extract_features(
        self,
        budget: float,
        impressions: float,
        predicted_ctr_pct: float,
        conversion_rate_pct: float,
        average_order_value: float,
        channel: str = "Meta Ads"
    ) -> Dict[str, float]:
        """
        Extract numerical features including log budget and impression scale.

        Args:
            budget: Campaign budget in USD.
            impressions: Target impressions reach.
            predicted_ctr_pct: CTR percentage.
            conversion_rate_pct: Landing page conversion rate %.
            average_order_value: Order value in USD.
            channel: Marketing channel string.

        Returns:
            Dictionary of numerical features.
        """
        log_budget = float(np.log1p(budget))
        log_impressions = float(np.log1p(impressions))
        expected_clicks = impressions * (predicted_ctr_pct / 100.0)
        expected_conversions = expected_clicks * (conversion_rate_pct / 100.0)

        return {
            "budget": float(budget),
            "log_budget": log_budget,
            "impressions": float(impressions),
            "log_impressions": log_impressions,
            "predicted_ctr_pct": float(predicted_ctr_pct),
            "conversion_rate_pct": float(conversion_rate_pct),
            "average_order_value": float(average_order_value),
            "expected_clicks": float(expected_clicks),
            "expected_conversions": float(expected_conversions)
        }

    def transform_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform raw campaign parameter DataFrame into feature DataFrame.

        Args:
            df: Input DataFrame.

        Returns:
            Feature DataFrame.
        """
        records = []
        for idx, row in df.iterrows():
            f = self.extract_features(
                budget=float(row.get("budget", 1000.0)),
                impressions=float(row.get("impressions", 50000.0)),
                predicted_ctr_pct=float(row.get("predicted_ctr_pct", 1.5)),
                conversion_rate_pct=float(row.get("conversion_rate_pct", 2.0)),
                average_order_value=float(row.get("average_order_value", 100.0)),
                channel=str(row.get("channel", "Meta Ads"))
            )
            f["channel"] = str(row.get("channel", "Meta Ads"))
            records.append(f)

        return pd.DataFrame(records)


if __name__ == "__main__":
    extractor = ROIFeatureExtractor()
    df_sample = pd.DataFrame([{"budget": 5000.0, "impressions": 200000.0, "predicted_ctr_pct": 2.0}])
    print(extractor.transform_dataframe(df_sample))
