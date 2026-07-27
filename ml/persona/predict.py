"""
Persona Predictor (`ml/persona/predict.py`).

Inference class for assigning new customer feedback samples to personas/clusters.
"""

import logging
import os
import sys
from typing import Dict, Any, Optional
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from ml.persona.features import PersonaFeatureExtractor
from ml.persona.model import PersonaClusteringModel
from ml.persona.preprocess import PersonaPreprocessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PersonaPredictor:
    """Predictor service assigning target customer samples to learned persona clusters."""

    ARCHETYPE_MAP = {
        0: "Technical Developer Persona",
        1: "Executive / Enterprise Buyer",
        2: "Growth Specialist / Consumer"
    }

    def __init__(self, model_dir: Optional[str] = None) -> None:
        """
        Initialize PersonaPredictor.

        Args:
            model_dir: Artifacts directory containing preprocessor.pkl and model.pkl.
        """
        if model_dir is None:
            model_dir = os.path.dirname(__file__)

        self.model_dir = model_dir
        self.extractor = PersonaFeatureExtractor()

        prep_path = os.path.join(self.model_dir, "preprocessor.pkl")
        model_path = os.path.join(self.model_dir, "model.pkl")

        if os.path.exists(prep_path) and os.path.exists(model_path):
            self.preprocessor = PersonaPreprocessor.load(prep_path)
            self.model = PersonaClusteringModel.load(model_path)
        else:
            logger.info("Persona artifacts missing. Training synthetic persona model...")
            from ml.persona.train import train_persona_pipeline
            train_persona_pipeline(artifact_dir=self.model_dir)
            self.preprocessor = PersonaPreprocessor.load(prep_path)
            self.model = PersonaClusteringModel.load(model_path)

    def predict_persona(self, text: str, activity_score: float = 1.0) -> Dict[str, Any]:
        """
        Predict cluster assignment and archetype name for input text snippet.

        Args:
            text: Customer review snippet.
            activity_score: User activity metric score.

        Returns:
            Dictionary containing cluster_id and archetype name.
        """
        df_raw = pd.DataFrame([{"text": text, "activity_score": activity_score}])
        feat_df = self.extractor.transform_dataframe(df_raw)
        X = self.preprocessor.transform(feat_df, df_raw["text"])

        cluster_id = int(self.model.predict(X)[0])
        archetype = self.ARCHETYPE_MAP.get(cluster_id, f"Customer Segment {cluster_id + 1}")

        return {
            "text": text,
            "cluster_id": cluster_id,
            "archetype_name": archetype
        }


if __name__ == "__main__":
    predictor = PersonaPredictor()
    result = predictor.predict_persona("Need webhook integration and faster API response for python sdk.")
    print("Inference Result:", result)
