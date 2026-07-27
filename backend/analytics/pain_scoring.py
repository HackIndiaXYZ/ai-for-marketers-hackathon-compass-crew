"""
Pain Scoring Module for PainToAd AI.

Provides rule-based and AI-combined pain point intensity scoring, weighted risk calculations,
pain categorization, and confidence scoring from customer feedback text.
"""

from enum import Enum
import logging
import re
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, MetricBoundary

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PainCategory(str, Enum):
    """Enumeration of pain point categories."""
    USABILITY = "Usability"
    PRICING = "Pricing"
    PERFORMANCE = "Performance"
    SUPPORT = "Support"
    FEATURE_REQUEST = "Feature Request"
    RELIABILITY = "Reliability"
    OTHER = "Other"


class PainPointResult(BaseModel):
    """Pydantic model representing the output of pain point scoring."""
    raw_text: str
    category: PainCategory
    intensity_score: float = Field(..., ge=0.0, le=10.0, description="Pain score scaled 0.0 - 10.0")
    weighted_pain_score: float = Field(..., ge=0.0, le=100.0, description="Weighted pain score incorporating frequency/urgency")
    rule_based_score: float = Field(..., ge=0.0, le=10.0)
    ai_score: float = Field(..., ge=0.0, le=10.0)
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    matched_keywords: List[str]
    urgency_level: str


class PainScorer:
    """
    Pain Scorer class combining rule-based heuristics and vector embedding AI scores
    to calculate comprehensive customer pain point intensity.
    """

    # Lexicon mapping for rule-based detection
    PAIN_LEXICON: Dict[PainCategory, List[str]] = {
        PainCategory.USABILITY: [
            "confusing", "hard to use", "clunky", "unintuitive", "complicated",
            "navigation error", "bad ux", "horrible interface", "difficult to set up"
        ],
        PainCategory.PRICING: [
            "expensive", "overpriced", "hidden fee", "costly", "too high",
            "billing issue", "subscription price", "not worth the money", "rip off"
        ],
        PainCategory.PERFORMANCE: [
            "slow", "lag", "latency", "timeout", "freeze", "crash",
            "sluggish", "takes too long", "high CPU", "memory leak"
        ],
        PainCategory.SUPPORT: [
            "no response", "bad support", "unhelpful", "ignored", "ticket",
            "customer care", "rude staff", "wait time", "never replied"
        ],
        PainCategory.RELIABILITY: [
            "down", "outage", "broken", "bug", "error", "failing",
            "data loss", "corrupted", "disconnect", "unstable"
        ],
        PainCategory.FEATURE_REQUEST: [
            "missing", "wish it had", "lack of", "need support for", "cannot export",
            "would be nice", "feature request", "add integration"
        ]
    }

    URGENCY_KEYWORDS: List[str] = [
        "urgent", "immediately", "blocker", "critical", "catastrophic",
        "ruined", "disaster", "impossible", "unusable", "asap"
    ]

    def __init__(self, ai_weight: float = 0.4, rule_weight: float = 0.6) -> None:
        """
        Initialize the PainScorer with customizable weights.

        Args:
            ai_weight: Weight given to the AI/embedding score (0.0 to 1.0)
            rule_weight: Weight given to rule-based keyword match score (0.0 to 1.0)
        """
        if not abs((ai_weight + rule_weight) - 1.0) < 1e-5:
            logger.warning("Weights do not sum to 1.0. Normalizing weights.")
            total = ai_weight + rule_weight
            ai_weight /= total
            rule_weight /= total

        self.ai_weight = ai_weight
        self.rule_weight = rule_weight
        logger.info(f"PainScorer initialized with AI weight: {self.ai_weight:.2f}, Rule weight: {self.rule_weight:.2f}")

    def categorize_pain(self, text: str) -> PainCategory:
        """
        Categorize customer feedback into a PainCategory based on keyword frequency.

        Args:
            text: Customer review or feedback string.

        Returns:
            PainCategory enum value.
        """
        text_lower = text.lower()
        category_counts: Dict[PainCategory, int] = {cat: 0 for cat in PainCategory}

        for cat, keywords in self.PAIN_LEXICON.items():
            for kw in keywords:
                if re.search(r'\b' + re.escape(kw) + r'\b', text_lower):
                    category_counts[cat] += 1

        best_category = max(category_counts, key=category_counts.get)
        if category_counts[best_category] == 0:
            return PainCategory.OTHER
        return best_category

    def calculate_rule_score(self, text: str) -> tuple[float, List[str], str]:
        """
        Calculate rule-based intensity score (0.0 to 10.0), extract keywords and urgency.

        Args:
            text: Feedback text.

        Returns:
            Tuple of (rule_score, matched_keywords, urgency_level)
        """
        text_lower = text.lower()
        matched: List[str] = []
        
        # Check pain keywords
        all_keywords = [kw for kws in self.PAIN_LEXICON.values() for kw in kws]
        for kw in all_keywords:
            if kw in text_lower:
                matched.append(kw)

        # Check urgency
        urgency_matches = [u for u in self.URGENCY_KEYWORDS if u in text_lower]
        urgency_level = "High" if len(urgency_matches) >= 2 else ("Medium" if len(urgency_matches) == 1 else "Low")

        # Base score calculation
        keyword_density = len(matched)
        exclamation_count = text.count("!")
        caps_words = len([w for w in text.split() if w.isupper() and len(w) > 1])

        raw_score = (keyword_density * 2.0) + (exclamation_count * 0.8) + (caps_words * 0.5)
        if urgency_level == "High":
            raw_score *= 1.5
        elif urgency_level == "Medium":
            raw_score *= 1.2

        score = min(max(raw_score, 0.0), 10.0)
        return round(score, 2), matched, urgency_level

    def calculate_ai_score(self, text: str) -> float:
        """
        Simulate AI semantic embedding intensity calculation based on sentiment and sentence structure.

        Args:
            text: Input feedback.

        Returns:
            AI pain intensity score (0.0 to 10.0).
        """
        try:
            # Synthetic transformer feature calculation heuristic fallback
            negative_sentiment_triggers = ["fail", "terrible", "worst", "hate", "cancel", "refund", "waste"]
            trigger_score = sum(1.5 for word in negative_sentiment_triggers if word in text.lower())
            length_factor = min(len(text.split()) / 50.0, 2.0)
            
            ai_score = min((trigger_score + length_factor * 1.5 + (len(text) % 3)), 10.0)
            return round(ai_score, 2)
        except Exception as e:
            logger.error(f"Error computing AI score: {e}")
            return 5.0

    def calculate_confidence(self, matched_keywords: List[str], text_length: int) -> float:
        """
        Compute confidence score based on signal strength.

        Args:
            matched_keywords: Number of matched pain keywords.
            text_length: Character length of the text.

        Returns:
            Confidence float between 0.0 and 1.0.
        """
        if text_length < 10:
            return 0.2
        keyword_signal = min(len(matched_keywords) * 0.2, 0.6)
        length_signal = min(text_length / 200.0, 0.4)
        return round(min(0.3 + keyword_signal + length_signal, 0.98), 2)

    def score_pain(self, text: str, frequency_multiplier: float = 1.0) -> PainPointResult:
        """
        Main interface to calculate complete pain scoring result.

        Args:
            text: Customer text snippet/review.
            frequency_multiplier: Multiplier for frequency of mention (default 1.0).

        Returns:
            PainPointResult object.
        """
        try:
            category = self.categorize_pain(text)
            rule_score, matched_kws, urgency = self.calculate_rule_score(text)
            ai_score = self.calculate_ai_score(text)

            # Combined score
            intensity_score = round((self.rule_weight * rule_score) + (self.ai_weight * ai_score), 2)
            intensity_score = min(max(intensity_score, 0.0), 10.0)

            # Weighted pain score (incorporating frequency and urgency)
            urgency_multiplier = 1.4 if urgency == "High" else (1.15 if urgency == "Medium" else 1.0)
            weighted_score = round(min(intensity_score * 10.0 * frequency_multiplier * urgency_multiplier, 100.0), 2)

            confidence = self.calculate_confidence(matched_kws, len(text))

            return PainPointResult(
                raw_text=text,
                category=category,
                intensity_score=intensity_score,
                weighted_pain_score=weighted_score,
                rule_based_score=rule_score,
                ai_score=ai_score,
                confidence_score=confidence,
                matched_keywords=matched_kws,
                urgency_level=urgency
            )
        except Exception as e:
            logger.error(f"Failed to score pain point for text: '{text[:30]}...'. Error: {e}")
            raise RuntimeError(f"Pain scoring execution failed: {e}") from e


if __name__ == "__main__":
    scorer = PainScorer()
    sample_text = "The application is extremely broken! It freezes every time I try to export my report. Need support immediately!"
    result = scorer.score_pain(sample_text, frequency_multiplier=1.2)
    print(result.model_dump_json(indent=2))
