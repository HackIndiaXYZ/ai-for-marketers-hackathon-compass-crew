"""
Sentiment Training Script (`ml/sentiment/train.py`).

Trains multi-label emotion classifier and sentiment polarity regressor and saves artifacts.
"""

import logging
import os
import sys
from sklearn.model_selection import train_test_split

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from ml.sentiment.features import SentimentFeatureExtractor
from ml.sentiment.model import SentimentEmotionModel
from ml.sentiment.preprocess import SentimentPreprocessor
from ml.sentiment.utils import evaluate_multilabel_metrics, generate_synthetic_sentiment_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def train_sentiment_pipeline(artifact_dir: str = None) -> None:
    """
    Train and save Sentiment & Emotion ML pipeline artifacts.

    Args:
        artifact_dir: Output directory path.
    """
    if artifact_dir is None:
        artifact_dir = os.path.dirname(__file__)

    os.makedirs(artifact_dir, exist_ok=True)
    logger.info("Starting Sentiment ML Training Pipeline...")

    # 1. Load Data
    df = generate_synthetic_sentiment_data(n_samples=300)
    logger.info(f"Loaded {len(df)} samples for training.")

    # 2. Extract Lexicon Features
    extractor = SentimentFeatureExtractor()
    feat_df = extractor.transform_dataframe(df, text_column="text")

    # 3. Preprocess
    preprocessor = SentimentPreprocessor()
    X = preprocessor.fit_transform(feat_df, df["text"])

    emotion_cols = ["joy", "anger", "sadness", "fear", "frustration"]
    y_emotions = df[emotion_cols].values
    y_polarity = df["polarity"].values

    # 4. Train / Test Split
    X_train, X_test, y_emo_train, y_emo_test, y_pol_train, y_pol_test = train_test_split(
        X, y_emotions, y_polarity, test_size=0.2, random_state=42
    )

    # 5. Fit Model
    model = SentimentEmotionModel()
    model.fit(X_train, y_emo_train, y_pol_train)

    # 6. Evaluate
    emo_preds, pol_preds = model.predict(X_test)
    metrics = evaluate_multilabel_metrics(y_emo_test, emo_preds)
    logger.info(f"Emotion Multi-Label Evaluation: {metrics}")

    # 7. Save Artifacts
    model_path = os.path.join(artifact_dir, "model.pkl")
    prep_path = os.path.join(artifact_dir, "preprocessor.pkl")

    model.save(model_path)
    preprocessor.save(prep_path)
    logger.info("Sentiment ML Training Pipeline successfully completed.")


if __name__ == "__main__":
    train_sentiment_pipeline()
