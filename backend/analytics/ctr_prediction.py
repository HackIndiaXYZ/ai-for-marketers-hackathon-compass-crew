"""
CTR Prediction Analytics Module for PainToAd AI.

Provides high-level backend analytics wrapper for evaluating ad copy, calculating predicted Click-Through-Rate (CTR),
evaluating copy hooks, channel compatibility, confidence bounds, and optimization recommendations.
"""

import logging
import os
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, MetricBoundary

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CTRPredictionRequest(BaseModel):
    """Payload for CTR evaluation request."""
    headline: str = Field(..., min_length=3, description="Ad headline text")
    body_text: str = Field("", description="Main ad copy body")
    target_platform: str = Field("Meta", description="Platform: Meta, Google, LinkedIn, Twitter, Email")
    target_audience: str = Field("B2B Professionals", description="Target customer segment")
    call_to_action: str = Field("Learn More", description="CTA text")


class CTRPredictionResponse(BaseModel):
    """Response payload for CTR evaluation."""
    headline: str
    target_platform: str
    predicted_ctr_pct: float = Field(..., ge=0.0, le=100.0, description="Predicted CTR percentage")
    benchmark_ctr_pct: float = Field(..., description="Industry benchmark CTR for platform")
    performance_tier: str = Field(..., description="Above Average, Average, Below Average")
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    copy_quality_score: float = Field(..., ge=0.0, le=10.0)
    recommendations: List[str]


class CTRPredictionService:
    """
    CTR Prediction Service handling ad copy feature extraction, machine learning model scoring,
    benchmark comparison, and optimization recommendations.
    """

    PLATFORM_BENCHMARKS: Dict[str, float] = {
        "Meta": 1.25,
        "Google": 3.17,
        "LinkedIn": 0.65,
        "Twitter": 0.86,
        "Email": 2.50
    }

    POWER_WORDS: List[str] = [
        "free", "instant", "guaranteed", "secret", "proven", "boost",
        "save", "effortless", "unlock", "exclusive", "now", "stop", "transform"
    ]

    def __init__(self, model_dir: Optional[str] = None) -> None:
        """
        Initialize CTR Prediction Service with optional model directory.

        Args:
            model_dir: Path to directory containing trained ML model artifacts.
        """
        self.model_dir = model_dir or os.path.join(os.path.dirname(__file__), "..", "..", "ml", "ctr_prediction")
        self.ml_model = None
        self._load_ml_model()

    def _load_ml_model(self) -> None:
        """Attempt to load trained ML pipeline or fall back gracefully to heuristic scoring."""
        try:
            # Dynamic import of ml package predictor if trained model exists
            from ml.ctr_prediction.predict import CTRPredictor
            self.ml_model = CTRPredictor(model_dir=self.model_dir)
            logger.info("Loaded ML CTRPredictor model successfully.")
        except Exception as e:
            logger.warning(f"Could not load ML CTRPredictor ({e}). Using rule-augmented estimator.")
            self.ml_model = None

    def evaluate_copy_quality(self, headline: str, body_text: str, cta: str) -> Tuple[float, List[str]]:
        """
        Evaluate ad copy quality based on power words, sentiment, length, and call-to-action strength.

        Args:
            headline: Headline string.
            body_text: Body copy string.
            cta: Call-to-action string.

        Returns:
            Tuple of (quality_score 0-10, list of recommendations)
        """
        score = 5.0
        recommendations: List[str] = []

        combined = f"{headline} {body_text} {cta}".lower()
        word_count = len(headline.split())

        # Headline length check
        if 5 <= word_count <= 9:
            score += 1.5
        elif word_count < 4:
            score -= 1.0
            recommendations.append("Expand headline length to 5-9 words for maximum engagement.")
        elif word_count > 12:
            score -= 1.0
            recommendations.append("Shorten headline under 10 words to prevent truncation.")

        # Power words check
        matched_power = [w for w in self.POWER_WORDS if w in combined]
        if matched_power:
            score += min(len(matched_power) * 0.8, 2.0)
        else:
            recommendations.append("Include power words like 'proven', 'transform', or 'instant' to boost engagement.")

        # Question mark hook
        if "?" in headline:
            score += 0.8

        # Call to action evaluation
        if any(action in cta.lower() for action in ["get", "start", "try", "claim", "download"]):
            score += 1.0
        else:
            recommendations.append("Use active verbs in CTA (e.g. 'Get Started', 'Claim Trial').")

        return round(min(max(score, 1.0), 10.0), 2), recommendations

    def predict_ctr(self, request: CTRPredictionRequest) -> CTRPredictionResponse:
        """
        Predict CTR percentage for input request.

        Args:
            request: CTRPredictionRequest object.

        Returns:
            CTRPredictionResponse object.
        """
        try:
            benchmark = self.PLATFORM_BENCHMARKS.get(request.target_platform, 1.50)
            quality_score, recs = self.evaluate_copy_quality(
                request.headline, request.body_text, request.call_to_action
            )

            # ML model inference if available
            if self.ml_model is not None:
                try:
                    predicted_ctr, confidence = self.ml_model.predict_single(
                        headline=request.headline,
                        body_text=request.body_text,
                        platform=request.target_platform,
                        cta=request.call_to_action
                    )
                except Exception as ml_err:
                    logger.error(f"ML Predictor call failed: {ml_err}. Falling back to baseline formula.")
                    predicted_ctr = benchmark * (quality_score / 6.0)
                    confidence = 0.70
            else:
                # Baseline physics model formula
                multiplier = quality_score / 6.0
                predicted_ctr = benchmark * multiplier
                confidence = 0.75

            predicted_ctr = round(min(max(predicted_ctr, 0.1), 15.0), 2)

            # Performance tier comparison
            if predicted_ctr >= benchmark * 1.2:
                tier = "Above Average"
            elif predicted_ctr <= benchmark * 0.8:
                tier = "Below Average"
            else:
                tier = "Average"

            return CTRPredictionResponse(
                headline=request.headline,
                target_platform=request.target_platform,
                predicted_ctr_pct=predicted_ctr,
                benchmark_ctr_pct=benchmark,
                performance_tier=tier,
                confidence_score=confidence,
                copy_quality_score=quality_score,
                recommendations=recs
            )

        except Exception as e:
            logger.error(f"Failed to calculate CTR prediction: {e}")
            raise RuntimeError(f"CTR Prediction execution error: {e}") from e


if __name__ == "__main__":
    service = CTRPredictionService()
    req = CTRPredictionRequest(
        headline="Transform Your Marketing ROI in 30 Days!",
        body_text="Automate customer pain detection and campaign creation with PainToAd AI.",
        target_platform="Meta",
        call_to_action="Get Started Free"
    )
    res = service.predict_ctr(req)
    print(res.model_dump_json(indent=2))
