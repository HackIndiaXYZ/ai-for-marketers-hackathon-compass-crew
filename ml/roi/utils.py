"""
ROI Utilities (`ml/roi/utils.py`).

Provides evaluation metrics (RMSE, MAE, R2, MAPE) and synthetic ROI training data generator.
"""

import logging
from typing import Dict
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def evaluate_roi_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """
    Calculate regression evaluation metrics for ROI revenue forecasting.

    Args:
        y_true: True revenue.
        y_pred: Predicted revenue.

    Returns:
        Dictionary of metrics.
    """
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    mae = float(mean_absolute_error(y_true, y_pred))
    r2 = float(r2_score(y_true, y_pred))
    mape = float(np.mean(np.abs((y_true - y_pred) / np.maximum(y_true, 1.0))) * 100.0)

    return {
        "rmse": round(rmse, 2),
        "mae": round(mae, 2),
        "r2": round(r2, 4),
        "mape_pct": round(mape, 2)
    }


def generate_synthetic_roi_data(n_samples: int = 300) -> pd.DataFrame:
    """
    Generate synthetic campaign performance dataset for training ROI model.

    Args:
        n_samples: Number of samples.

    Returns:
        Pandas DataFrame.
    """
    np.random.seed(42)
    channels = ["Meta Ads", "Google Ads", "LinkedIn Ads", "Email Marketing"]

    data = []
    for _ in range(n_samples):
        budget = float(np.random.uniform(500.0, 20000.0))
        impressions = budget * np.random.uniform(30.0, 70.0)
        ctr = float(np.random.uniform(0.8, 3.5))
        conv_rate = float(np.random.uniform(1.5, 4.5))
        aov = float(np.random.uniform(50.0, 250.0))
        ch = str(np.random.choice(channels))

        # Expected revenue simulation formula
        clicks = impressions * (ctr / 100.0)
        conversions = clicks * (conv_rate / 100.0)
        base_rev = conversions * aov

        # Add noise
        noise = np.random.normal(1.0, 0.1)
        rev = round(float(base_rev * noise), 2)

        data.append({
            "budget": round(budget, 2),
            "impressions": round(impressions, 0),
            "predicted_ctr_pct": round(ctr, 2),
            "conversion_rate_pct": round(conv_rate, 2),
            "average_order_value": round(aov, 2),
            "channel": ch,
            "revenue": max(0.0, rev)
        })

    return pd.DataFrame(data)


if __name__ == "__main__":
    df = generate_synthetic_roi_data(5)
    print("Synthetic ROI Data Head:\n", df.head(3))
