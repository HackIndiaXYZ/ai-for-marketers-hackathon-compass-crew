"""
CTR Utilities Module (`ml/ctr_prediction/utils.py`).

Provides evaluation metrics, synthetic benchmark dataset generation, and artifact loading helpers.
"""

import logging
from typing import Dict, Tuple
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def evaluate_regression_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """
    Calculate regression metrics: RMSE, MAE, R2.

    Args:
        y_true: True ground truth values.
        y_pred: Predicted values.

    Returns:
        Dictionary of computed metrics.
    """
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    mae = float(mean_absolute_error(y_true, y_pred))
    r2 = float(r2_score(y_true, y_pred))

    return {
        "rmse": round(rmse, 4),
        "mae": round(mae, 4),
        "r2": round(r2, 4)
    }


def generate_synthetic_ctr_data(n_samples: int = 300) -> pd.DataFrame:
    """
    Generate synthetic benchmark dataset for training CTR models.

    Args:
        n_samples: Number of rows to generate.

    Returns:
        Pandas DataFrame.
    """
    np.random.seed(42)
    headlines = [
        "Boost Your Marketing ROI Today!",
        "Transform Customer Feedback into Sales",
        "Stop Wasting Budget on Unused Tools",
        "The Secret Strategy for Higher Conversions",
        "Automate Customer Analytics Effortlessly"
    ]
    bodies = [
        "Sign up now for our 14-day free trial.",
        "Join 10,000+ top marketing professionals.",
        "Get instant setup in under 5 minutes.",
        "Discover actionable intelligence today."
    ]
    platforms = ["Meta", "Google", "LinkedIn", "Twitter"]
    ctas = ["Learn More", "Get Started", "Claim Free Trial", "Download Now"]

    data = []
    for _ in range(n_samples):
        h = np.random.choice(headlines)
        b = np.random.choice(bodies)
        p = np.random.choice(platforms)
        c = np.random.choice(ctas)

        # Baseline CTR simulation formula
        base = 1.2 if p == "Meta" else (2.8 if p == "Google" else 0.8)
        boost = 0.5 if "Free" in c or "Now" in h else 0.0
        ctr = round(float(np.random.normal(base + boost, 0.4)), 2)
        ctr = max(0.1, ctr)

        data.append({
            "headline": h,
            "body_text": b,
            "platform": p,
            "cta": c,
            "ctr": ctr
        })

    return pd.DataFrame(data)


if __name__ == "__main__":
    df = generate_synthetic_ctr_data(10)
    print("Synthetic Data Head:\n", df.head(3))
