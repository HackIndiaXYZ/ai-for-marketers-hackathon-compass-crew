"""
Persona Clustering Model (`ml/persona/model.py`).

KMeans and Agglomerative Clustering model for customer persona segmentation.
"""

import logging
from typing import Dict, List, Tuple
import joblib
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PersonaClusteringModel:
    """KMeans Clustering Model for segmenting customer target personas."""

    def __init__(self, n_clusters: int = 3) -> None:
        """
        Initialize KMeans model.

        Args:
            n_clusters: Number of clusters (personas).
        """
        self.n_clusters = n_clusters
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.is_trained = False
        logger.info(f"PersonaClusteringModel initialized (n_clusters={n_clusters}).")

    def fit(self, X: np.ndarray) -> "PersonaClusteringModel":
        """
        Fit KMeans model on feature matrix.

        Args:
            X: Feature matrix.

        Returns:
            Fitted model instance.
        """
        logger.info(f"Fitting PersonaClusteringModel on {X.shape[0]} samples...")
        self.kmeans.fit(X)
        self.is_trained = True
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Assign cluster IDs for input samples.

        Args:
            X: Feature matrix.

        Returns:
            Array of cluster label integers.
        """
        if not self.is_trained:
            raise RuntimeError("PersonaClusteringModel must be trained before predict.")
        return self.kmeans.predict(X)

    def calculate_silhouette(self, X: np.ndarray) -> float:
        """
        Calculate silhouette metric score.

        Args:
            X: Feature matrix.

        Returns:
            Silhouette score float (-1.0 to 1.0).
        """
        if X.shape[0] <= self.n_clusters:
            return 0.0
        labels = self.predict(X)
        return float(silhouette_score(X, labels))

    def save(self, filepath: str) -> None:
        """Save model artifact."""
        joblib.dump(self, filepath)
        logger.info(f"Saved PersonaClusteringModel to {filepath}")

    @staticmethod
    def load(filepath: str) -> "PersonaClusteringModel":
        """Load model artifact."""
        obj = joblib.load(filepath)
        logger.info(f"Loaded PersonaClusteringModel from {filepath}")
        return obj


if __name__ == "__main__":
    X_dummy = np.random.randn(30, 4)
    model = PersonaClusteringModel(n_clusters=3)
    model.fit(X_dummy)
    labels = model.predict(X_dummy[:5])
    print("Assigned Clusters:", labels)
