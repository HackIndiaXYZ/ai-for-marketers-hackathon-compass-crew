"""
CTR Model Training Script (`ml/ctr_prediction/train.py`).

Generates synthetic/benchmark datasets, preprocesses features, trains the CTR ensemble model,
evaluates metrics, and exports model artifacts.
"""

import logging
import os
import sys
from sklearn.model_selection import train_test_split

# Add root directory to sys.path if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from ml.ctr_prediction.features import CTRFeatureExtractor
from ml.ctr_prediction.model import CTRModel
from ml.ctr_prediction.preprocess import CTRPreprocessor
from ml.ctr_prediction.utils import evaluate_regression_metrics, generate_synthetic_ctr_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def train_ctr_pipeline(artifact_dir: str = None) -> None:
    """
    Train and save CTR ML artifacts.

    Args:
        artifact_dir: Output directory to save model and preprocessor artifacts.
    """
    if artifact_dir is None:
        artifact_dir = os.path.dirname(__file__)

    os.makedirs(artifact_dir, exist_ok=True)
    logger.info("Starting CTR Model Training Pipeline...")

    # 1. Generate / Load Data
    df = generate_synthetic_ctr_data(n_samples=400)
    logger.info(f"Loaded {len(df)} dataset samples for training.")

    # 2. Extract Features
    extractor = CTRFeatureExtractor()
    feat_df = extractor.transform_dataframe(df)

    # 3. Preprocess Features
    preprocessor = CTRPreprocessor()
    X = preprocessor.fit_transform(feat_df, df["headline"])
    y = df["ctr"].values

    # 4. Train / Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 5. Train Model
    model = CTRModel()
    model.fit(X_train, y_train)

    # 6. Evaluate
    y_pred = model.predict(X_test)
    metrics = evaluate_regression_metrics(y_test, y_pred)
    logger.info(f"Training Evaluation Metrics: {metrics}")

    # 7. Save Artifacts
    model_path = os.path.join(artifact_dir, "model.pkl")
    prep_path = os.path.join(artifact_dir, "preprocessor.pkl")

    model.save(model_path)
    preprocessor.save(prep_path)

    logger.info("CTR Training Pipeline successfully completed.")


if __name__ == "__main__":
    train_ctr_pipeline()
