"""
Emotion Analysis Module for PainToAd AI.

Provides multi-label emotion prediction, sentiment polarity classification,
emotional intensity scoring, and visualization dictionary output for charts.
"""

from enum import Enum
import logging
import math
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from textblob import TextBlob

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SentimentType(str, Enum):
    """Overall sentiment polarity."""
    POSITIVE = "Positive"
    NEGATIVE = "Negative"
    NEUTRAL = "Neutral"


class EmotionLabel(str, Enum):
    """Primary emotion labels."""
    JOY = "Joy"
    ANGER = "Anger"
    SADNESS = "Sadness"
    FEAR = "Fear"
    SURPRISE = "Surprise"
    FRUSTRATION = "Frustration"
    DISAPPOINTMENT = "Disappointment"
    TRUST = "Trust"


class EmotionAnalysisResult(BaseModel):
    """Pydantic payload for emotion analysis output."""
    raw_text: str
    sentiment: SentimentType
    polarity_score: float = Field(..., ge=-1.0, le=1.0)
    subjectivity_score: float = Field(..., ge=0.0, le=1.0)
    primary_emotion: EmotionLabel
    detected_emotions: List[EmotionLabel]
    emotion_probabilities: Dict[str, float]
    emotional_intensity: float = Field(..., ge=0.0, le=10.0)


class EmotionAnalyzer:
    """
    Emotion Analyzer performing multi-label detection, sentiment polarity evaluation,
    emotional intensity metrics, and chart dictionary helpers.
    """

    # Lexicon mapping for emotion indicators
    EMOTION_LEXICON: Dict[EmotionLabel, List[str]] = {
        EmotionLabel.JOY: ["love", "great", "awesome", "fantastic", "delighted", "happy", "excellent", "amazing", "wonderful"],
        EmotionLabel.ANGER: ["hate", "furious", "outraged", "mad", "disgusted", "annoyed", "ridiculous", "scam", "terrible"],
        EmotionLabel.SADNESS: ["sad", "depressing", "disappointed", "unfortunate", "regret", "upset", "sorry", "miserable"],
        EmotionLabel.FEAR: ["worried", "scared", "afraid", "risk", "security flaw", "vulnerable", "anxious", "terrified"],
        EmotionLabel.SURPRISE: ["shocked", "unexpected", "surprised", "astonished", "wow", "unbelievable"],
        EmotionLabel.FRUSTRATION: ["frustrating", "stuck", "painful", "impossible", "waste of time", "horrible experience", "clunky"],
        EmotionLabel.DISAPPOINTMENT: ["let down", "underwhelmed", "expected better", "lacking", "poor quality", "useless"],
        EmotionLabel.TRUST: ["reliable", "secure", "trusted", "dependable", "consistent", "authentic", "safe"]
    }

    def __init__(self, probability_threshold: float = 0.15) -> None:
        """
        Initialize EmotionAnalyzer.

        Args:
            probability_threshold: Minimum probability to include an emotion in detected_emotions.
        """
        self.threshold = probability_threshold
        logger.info(f"EmotionAnalyzer initialized with threshold: {self.threshold}")

    def analyze_sentiment(self, text: str) -> tuple[SentimentType, float, float]:
        """
        Calculate sentiment polarity and subjectivity using TextBlob.

        Args:
            text: Input string.

        Returns:
            Tuple of (SentimentType, polarity [-1, 1], subjectivity [0, 1])
        """
        try:
            blob = TextBlob(text)
            polarity = float(blob.sentiment.polarity)
            subjectivity = float(blob.sentiment.subjectivity)

            if polarity > 0.1:
                sentiment = SentimentType.POSITIVE
            elif polarity < -0.1:
                sentiment = SentimentType.NEGATIVE
            else:
                sentiment = SentimentType.NEUTRAL

            return sentiment, round(polarity, 3), round(subjectivity, 3)
        except Exception as e:
            logger.error(f"Error during sentiment calculation: {e}")
            return SentimentType.NEUTRAL, 0.0, 0.0

    def compute_emotion_probabilities(self, text: str, polarity: float, subjectivity: float) -> Dict[str, float]:
        """
        Compute softmax normalized probability distribution across emotion labels.

        Args:
            text: Raw input text.
            polarity: Text sentiment polarity.
            subjectivity: Text subjectivity.

        Returns:
            Dictionary mapping emotion names to probability values summing to 1.0.
        """
        text_lower = text.lower()
        raw_scores: Dict[str, float] = {e.value: 0.1 for e in EmotionLabel}

        # Count keyword hits
        for emotion, keywords in self.EMOTION_LEXICON.items():
            count = sum(1 for kw in keywords if kw in text_lower)
            raw_scores[emotion.value] += count * 2.0

        # Adjust based on sentiment polarity
        if polarity < -0.2:
            raw_scores[EmotionLabel.FRUSTRATION.value] += 1.5
            raw_scores[EmotionLabel.ANGER.value] += 1.2
            raw_scores[EmotionLabel.DISAPPOINTMENT.value] += 1.0
        elif polarity > 0.2:
            raw_scores[EmotionLabel.JOY.value] += 2.0
            raw_scores[EmotionLabel.TRUST.value] += 1.2

        # Softmax transformation
        exp_scores = {k: math.exp(v) for k, v in raw_scores.items()}
        sum_exp = sum(exp_scores.values())
        probabilities = {k: round(v / sum_exp, 4) for k, v in exp_scores.items()}

        return probabilities

    def calculate_emotional_intensity(self, text: str, polarity: float, subjectivity: float) -> float:
        """
        Calculate overall emotional intensity (0.0 to 10.0 scale).

        Args:
            text: Input string.
            polarity: Sentiment polarity.
            subjectivity: Sentiment subjectivity.

        Returns:
            Emotional intensity score scaled 0.0 to 10.0.
        """
        exclamation_weight = min(text.count("!") * 1.5, 3.0)
        caps_weight = min(sum(1 for w in text.split() if w.isupper() and len(w) > 1) * 1.0, 3.0)
        polarity_magnitude = abs(polarity) * 4.0
        subjectivity_weight = subjectivity * 2.0

        intensity = polarity_magnitude + subjectivity_weight + exclamation_weight + caps_weight
        return round(min(max(intensity, 0.0), 10.0), 2)

    def analyze(self, text: str) -> EmotionAnalysisResult:
        """
        Main execution point for multi-label emotion and sentiment analysis.

        Args:
            text: Customer text snippet.

        Returns:
            EmotionAnalysisResult object.
        """
        if not text or not text.strip():
            logger.warning("Empty text string provided to EmotionAnalyzer.")
            return EmotionAnalysisResult(
                raw_text="",
                sentiment=SentimentType.NEUTRAL,
                polarity_score=0.0,
                subjectivity_score=0.0,
                primary_emotion=EmotionLabel.TRUST,
                detected_emotions=[],
                emotion_probabilities={e.value: 0.125 for e in EmotionLabel},
                emotional_intensity=0.0
            )

        sentiment, polarity, subjectivity = self.analyze_sentiment(text)
        probabilities = self.compute_emotion_probabilities(text, polarity, subjectivity)
        intensity = self.calculate_emotional_intensity(text, polarity, subjectivity)

        # Primary emotion is the highest probability
        primary_str = max(probabilities, key=probabilities.get)
        primary_emotion = EmotionLabel(primary_str)

        # Multi-label detected emotions above threshold
        detected = [EmotionLabel(k) for k, v in probabilities.items() if v >= self.threshold]

        return EmotionAnalysisResult(
            raw_text=text,
            sentiment=sentiment,
            polarity_score=polarity,
            subjectivity_score=subjectivity,
            primary_emotion=primary_emotion,
            detected_emotions=detected,
            emotion_probabilities=probabilities,
            emotional_intensity=intensity
        )

    def get_plotly_chart_dict(self, result: EmotionAnalysisResult) -> Dict[str, Any]:
        """
        Helper method generating Plotly JSON configuration dictionary for radar chart visualization.

        Args:
            result: EmotionAnalysisResult instance.

        Returns:
            Plotly figure data and layout dictionary.
        """
        emotions = list(result.emotion_probabilities.keys())
        values = list(result.emotion_probabilities.values())

        return {
            "data": [
                {
                    "type": "scatterpolar",
                    "r": values,
                    "theta": emotions,
                    "fill": "toself",
                    "name": "Emotion Spectrum",
                    "marker": {"color": "#6366f1"}
                }
            ],
            "layout": {
                "polar": {
                    "radialaxis": {"visible": True, "range": [0, 1.0]}
                },
                "title": f"Emotional Intensity: {result.emotional_intensity}/10",
                "showlegend": False
            }
        }


if __name__ == "__main__":
    analyzer = EmotionAnalyzer()
    sample = "I am insanely frustrated with this platform! It crashes and I lost my work! Terrible service!"
    res = analyzer.analyze(sample)
    print(res.model_dump_json(indent=2))
