"""
ROI Model Training Script (`ml/roi/train.py`).

Fits feature preprocessor and ensemble regression model on campaign datasets and saves artifacts.
"""

import logging
import os
import sys
from sklearn.model_selection import train_test_split

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from ml.roi.features import ROIFeatureExtractor
from ml.roi.model import ROIPredictionModel
from ml.roi.preprocess import ROIPreprocessor
from ml.roi.utils import evaluate_roi_metrics, generate_synthetic_roi_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def train_roi_pipeline(artifact_dir: str = None) -> None:
    """
    Train and save ROI ML pipeline artifacts.

    Args:
        artifact_dir: Output directory path.
    """
    if artifact_dir is None:
        artifact_dir = os.path.dirname(__file__)

    os.makedirs(artifact_dir, exist_ok=True)
    logger.info("Starting ROI ML Training Pipeline...")

    # 1. Generate Data
    df = generate_synthetic_roi_data(n_samples=400)
    logger.info(f"Loaded {len(df)} campaign samples for ROI model training.")

    # 2. Extract Features
    extractor = ROIFeatureExtractor()
    feat_df = extractor.transform_dataframe(df)

    # 3. Preprocess
    preprocessor = ROIPreprocessor()
    X = preprocessor.fit_transform(feat_df)
    y = df["revenue"].values

    # 4. Train / Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 5. Fit Model
    model = ROIPredictionModel()
    model.fit(X_train, y_train)

    # 6. Evaluate
    y_pred = model.predict(X_test)
    metrics = evaluate_roi_metrics(y_test, y_pred)
    logger.info(f"ROI Training Evaluation Metrics: {metrics}")

    # 7. Save Artifacts
    model_path = os.path.join(artifact_dir, "model.pkl")
    prep_path = os.path.join(artifact_dir, "preprocessor.pkl")

    model.save(model_path)
    preprocessor.save(prep_path)
    logger.info("ROI ML Training Pipeline successfully completed.")


if __name__ == "__main__":
    train_roi_pipeline()
