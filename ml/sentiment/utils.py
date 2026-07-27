"""
Sentiment Utilities Module (`ml/sentiment/utils.py`).

Provides multi-label classification metrics (F1, Precision, Recall),
synthetic sentiment benchmark corpus generator, and mapping functions.
"""

import logging
from typing import Dict, List
import numpy as np
import pandas as pd
from sklearn.metrics import f1_score, precision_score, recall_score

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def evaluate_multilabel_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """
    Calculate F1, Precision, and Recall scores for multi-label emotion prediction.

    Args:
        y_true: True multi-label binary array.
        y_pred: Predicted binary array.

    Returns:
        Dictionary of metrics.
    """
    f1 = float(f1_score(y_true, y_pred, average='micro', zero_division=0))
    precision = float(precision_score(y_true, y_pred, average='micro', zero_division=0))
    recall = float(recall_score(y_true, y_pred, average='micro', zero_division=0))

    return {
        "micro_f1": round(f1, 4),
        "micro_precision": round(precision, 4),
        "micro_recall": round(recall, 4)
    }


def generate_synthetic_sentiment_data(n_samples: int = 250) -> pd.DataFrame:
    """
    Generate synthetic feedback text corpus for sentiment & emotion training.

    Args:
        n_samples: Number of samples.

    Returns:
        Pandas DataFrame.
    """
    np.random.seed(42)
    corpus = [
        ("I absolutely love this product! Amazing speed and intuitive UI.", "joy", 0.85),
        ("This platform is terrible! Crashes all the time, customer service is useless.", "anger", -0.90),
        ("I am really disappointed. Missing feature support and clunky UX.", "sadness", -0.60),
        ("Scared to store sensitive data here due to security vulnerabilities.", "fear", -0.40),
        ("Stuck on the export screen for hours! Impossible to finish my work.", "frustration", -0.75),
        ("Decent software, gets the job done but overpriced.", "disappointment", -0.10),
        ("Reliable and fast setup. Excellent support team!", "joy", 0.80)
    ]

    data = []
    for _ in range(n_samples):
        text, primary_emo, pol = corpus[np.random.choice(len(corpus))]
        # Multi-label binary encoding: ["joy", "anger", "sadness", "fear", "frustration"]
        emotions = [
            1 if primary_emo == "joy" else 0,
            1 if primary_emo == "anger" else 0,
            1 if primary_emo == "sadness" else 0,
            1 if primary_emo == "fear" else 0,
            1 if primary_emo in ["frustration", "anger"] else 0
        ]
        data.append({
            "text": text,
            "joy": emotions[0],
            "anger": emotions[1],
            "sadness": emotions[2],
            "fear": emotions[3],
            "frustration": emotions[4],
            "polarity": pol
        })

    return pd.DataFrame(data)


if __name__ == "__main__":
    df = generate_synthetic_sentiment_data(5)
    print("Synthetic Sentiment Data Head:\n", df.head(3))
