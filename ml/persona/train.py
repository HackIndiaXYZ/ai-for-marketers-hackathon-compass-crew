"""
Persona Training Script (`ml/persona/train.py`).

Fits preprocessor and KMeans clustering model on customer feedback vectors and exports model artifacts.
"""

import logging
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from ml.persona.features import PersonaFeatureExtractor
from ml.persona.model import PersonaClusteringModel
from ml.persona.preprocess import PersonaPreprocessor
from ml.persona.utils import derive_cluster_names, generate_synthetic_persona_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def train_persona_pipeline(artifact_dir: str = None, n_clusters: int = 3) -> None:
    """
    Train and save Persona Clustering ML pipeline.

    Args:
        artifact_dir: Output directory path.
        n_clusters: Number of target clusters.
    """
    if artifact_dir is None:
        artifact_dir = os.path.dirname(__file__)

    os.makedirs(artifact_dir, exist_ok=True)
    logger.info("Starting Persona ML Training Pipeline...")

    # 1. Load Data
    df = generate_synthetic_persona_data(n_samples=250)
    logger.info(f"Loaded {len(df)} customer samples for persona training.")

    # 2. Extract Features
    extractor = PersonaFeatureExtractor()
    feat_df = extractor.transform_dataframe(df)

    # 3. Preprocess
    preprocessor = PersonaPreprocessor(n_components=5)
    X = preprocessor.fit_transform(feat_df, df["text"])

    # 4. Fit Model
    model = PersonaClusteringModel(n_clusters=n_clusters)
    model.fit(X)

    # 5. Evaluate Silhouette Score
    sil_score = model.calculate_silhouette(X)
    logger.info(f"Persona Clustering Silhouette Score: {sil_score:.4f}")

    # 6. Derive Archetypes
    labels = model.predict(X)
    archetypes = derive_cluster_names(labels, df["text"].tolist())
    logger.info(f"Discovered Archetypes: {archetypes}")

    # 7. Save Artifacts
    model_path = os.path.join(artifact_dir, "model.pkl")
    prep_path = os.path.join(artifact_dir, "preprocessor.pkl")

    model.save(model_path)
    preprocessor.save(prep_path)
    logger.info("Persona ML Training Pipeline successfully completed.")


if __name__ == "__main__":
    train_persona_pipeline()
