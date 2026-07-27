"""
Persona Utilities (`ml/persona/utils.py`).

Provides cluster label generation heuristics, silhouette evaluation, and synthetic dataset generation.
"""

import logging
from typing import Dict, List
import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_synthetic_persona_data(n_samples: int = 200) -> pd.DataFrame:
    """
    Generate synthetic feedback dataset for persona clustering training.

    Args:
        n_samples: Sample size count.

    Returns:
        Pandas DataFrame.
    """
    np.random.seed(42)
    tech_feedback = [
        "API latency is too high, python SDK needs better documentation.",
        "Missing developer endpoints and webhook integration support.",
        "Code execution error on server startup."
    ]
    exec_feedback = [
        "Need enterprise security compliance and ROI dashboard reports.",
        "High subscription cost, need custom billing for enterprise scale.",
        "Team seat allocation and strategic account manager support required."
    ]
    consumer_feedback = [
        "Simple app, easy to use interface and good discount offers.",
        "Fast checkout and clean UI mobile experience.",
        "Wish it had cheaper monthly subscription options."
    ]

    data = []
    for _ in range(n_samples):
        r = np.random.rand()
        if r < 0.35:
            text = np.random.choice(tech_feedback)
            act = float(np.random.normal(4.5, 0.5))
        elif r < 0.70:
            text = np.random.choice(exec_feedback)
            act = float(np.random.normal(2.5, 0.5))
        else:
            text = np.random.choice(consumer_feedback)
            act = float(np.random.normal(1.2, 0.3))

        data.append({
            "text": text,
            "activity_score": max(0.5, act)
        })

    return pd.DataFrame(data)


def derive_cluster_names(labels: np.ndarray, texts: List[str]) -> Dict[int, str]:
    """
    Derive descriptive cluster archetype names based on keyword frequency in cluster snippets.

    Args:
        labels: Array of cluster integers.
        texts: Raw text snippets corresponding to samples.

    Returns:
        Dictionary mapping cluster ID to archetype title.
    """
    df = pd.DataFrame({"label": labels, "text": texts})
    cluster_names = {}

    for cluster_id, group in df.groupby("label"):
        combined = " ".join(group["text"]).lower()
        if "api" in combined or "code" in combined:
            cluster_names[cluster_id] = "Technical Developer Persona"
        elif "roi" in combined or "cost" in combined or "enterprise" in combined:
            cluster_names[cluster_id] = "Executive / Enterprise Buyer"
        else:
            cluster_names[cluster_id] = "Growth Specialist / Consumer"

    return cluster_names


if __name__ == "__main__":
    df = generate_synthetic_persona_data(10)
    print("Synthetic Data Head:\n", df.head(3))
