"""
Persona Builder Module for PainToAd AI.

Aggregates customer feedback clusters into detailed target audience personas,
inferring demographics, age groups, behavior patterns, pain profiles, and marketing angles.
"""

import logging
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BehavioralProfile(BaseModel):
    """Behavioral patterns and buying triggers for a persona."""
    primary_channels: List[str]
    buying_triggers: List[str]
    decision_drivers: List[str]
    risk_tolerance: str  # High, Medium, Low
    content_preference: List[str]


class CustomerPersona(BaseModel):
    """Comprehensive persona model."""
    persona_id: str
    name: str
    archetype: str
    inferred_age_group: str
    role_or_industry: str
    pain_profile: List[str]
    top_emotions: List[str]
    behavior: BehavioralProfile
    recommended_campaign_angle: str
    sample_ad_headline: str
    confidence_score: float = Field(..., ge=0.0, le=1.0)


class PersonaSummaryReport(BaseModel):
    """Collection report of personas derived from dataset."""
    total_customers_analyzed: int
    persona_count: int
    personas: List[CustomerPersona]


class PersonaBuilder:
    """
    Persona Builder constructing actionable customer personas from aggregated
    feedback, emotion distributions, pain points, and demographic signals.
    """

    AGE_GROUP_SIGNALS: Dict[str, List[str]] = {
        "18-24 (Gen Z)": ["tiktok", "discord", "cheap", "student", "fast", "vibes", "mobile app", "socials"],
        "25-34 (Millennials)": ["workplace", "career", "productivity", "saas", "dashboard", "efficiency", "flexible"],
        "35-49 (Gen X)": ["roi", "cost-effective", "security", "team management", "family", "reliable", "compliance"],
        "50+ (Boomers/Seniors)": ["phone support", "simple", "easy to read", "manual", "trustworthy", "traditional"]
    }

    ROLE_SIGNALS: Dict[str, List[str]] = {
        "Developer / Tech Lead": ["api", "code", "bug", "latency", "deployment", "github", "stack", "integration"],
        "Marketing Specialist": ["campaign", "ctr", "conversion", "leads", "ads", "social media", "roi", "copy"],
        "Executive / Founder": ["cost", "revenue", "scale", "strategic", "investor", "overhead", "growth", "margin"],
        "Product Manager": ["roadmap", "usability", "ux", "feature", "backlog", "user feedback", "analytics"],
        "General Consumer": ["price", "shipping", "quality", "refund", "store", "product", "discount"]
    }

    def __init__(self) -> None:
        """Initialize PersonaBuilder."""
        logger.info("PersonaBuilder initialized.")

    def infer_age_group(self, text_corpus: List[str]) -> str:
        """
        Infer likely age group demographic from text corpus signals.

        Args:
            text_corpus: Combined text snippets.

        Returns:
            Age group string label.
        """
        combined = " ".join(text_corpus).lower()
        scores: Dict[str, int] = {group: 0 for group in self.AGE_GROUP_SIGNALS}

        for group, keywords in self.AGE_GROUP_SIGNALS.items():
            for kw in keywords:
                scores[group] += combined.count(kw)

        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else "25-34 (Millennials)"

    def infer_role(self, text_corpus: List[str]) -> str:
        """
        Infer likely job role or customer segment from text corpus.

        Args:
            text_corpus: Combined text snippets.

        Returns:
            Role or industry title string.
        """
        combined = " ".join(text_corpus).lower()
        scores: Dict[str, int] = {role: 0 for role in self.ROLE_SIGNALS}

        for role, keywords in self.ROLE_SIGNALS.items():
            for kw in keywords:
                scores[role] += combined.count(kw)

        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else "Product / Marketing Professional"

    def derive_behavioral_profile(self, role: str, age_group: str) -> BehavioralProfile:
        """
        Derive behavioral patterns and buying triggers matching demographic profile.

        Args:
            role: Industry role.
            age_group: Age demographic.

        Returns:
            BehavioralProfile instance.
        """
        if "Developer" in role:
            return BehavioralProfile(
                primary_channels=["GitHub", "Reddit", "StackOverflow", "Twitter/X"],
                buying_triggers=["Integration speed", "Developer documentation", "API limits"],
                decision_drivers=["Technical capability", "System reliability", "Open source compatibility"],
                risk_tolerance="Medium",
                content_preference=["Code samples", "API docs", "Benchmark reports"]
            )
        elif "Executive" in role:
            return BehavioralProfile(
                primary_channels=["LinkedIn", "Email Newsletters", "Podcasts"],
                buying_triggers=["ROI proof", "Cost reduction", "Team scalability"],
                decision_drivers=["Revenue impact", "Enterprise security", "Customer references"],
                risk_tolerance="Low",
                content_preference=["Case studies", "ROI calculators", "Executive briefs"]
            )
        else:
            return BehavioralProfile(
                primary_channels=["Instagram", "LinkedIn", "Google Search"],
                buying_triggers=["Ease of use", "Immediate time-to-value", "Free trial"],
                decision_drivers=["Customer reviews", "Transparent pricing", "UI aesthetic"],
                risk_tolerance="High",
                content_preference=["Short video demos", "Interactive tours", "Comparison tables"]
            )

    def generate_persona(
        self,
        persona_id: str,
        cluster_name: str,
        feedback_samples: List[str],
        pain_points: List[str],
        emotions: List[str]
    ) -> CustomerPersona:
        """
        Generate a single CustomerPersona instance.

        Args:
            persona_id: Unique string ID.
            cluster_name: Descriptive name of customer cluster.
            feedback_samples: Raw customer text snippets.
            pain_points: Aggregated pain point labels.
            emotions: Top emotional tags.

        Returns:
            CustomerPersona Pydantic model.
        """
        try:
            age_group = self.infer_age_group(feedback_samples)
            role = self.infer_role(feedback_samples)
            behavior = self.derive_behavioral_profile(role, age_group)

            primary_pain = pain_points[0] if pain_points else "Efficiency Bottlenecks"
            campaign_angle = f"Eliminate {primary_pain} with automated precision tailored for {role}s."
            ad_headline = f"Stop Wasting Time on {primary_pain} — Try PainToAd AI Today."

            persona = CustomerPersona(
                persona_id=persona_id,
                name=f"{role.split('/')[0].strip()} {cluster_name}",
                archetype=cluster_name,
                inferred_age_group=age_group,
                role_or_industry=role,
                pain_profile=pain_points[:5],
                top_emotions=emotions[:4],
                behavior=behavior,
                recommended_campaign_angle=campaign_angle,
                sample_ad_headline=ad_headline,
                confidence_score=round(min(0.6 + len(feedback_samples) * 0.05, 0.95), 2)
            )
            return persona
        except Exception as e:
            logger.error(f"Failed to generate persona for cluster '{cluster_name}': {e}")
            raise RuntimeError(f"Persona generation failed: {e}") from e

    def build_persona_summary(self, clusters_data: List[Dict[str, Any]]) -> PersonaSummaryReport:
        """
        Build full summary report from multiple cluster dicts.

        Args:
            clusters_data: List of dicts with keys ('id', 'name', 'samples', 'pains', 'emotions').

        Returns:
            PersonaSummaryReport object.
        """
        personas: List[CustomerPersona] = []
        total_samples = 0

        for idx, item in enumerate(clusters_data):
            samples = item.get("samples", [])
            total_samples += len(samples)
            p = self.generate_persona(
                persona_id=item.get("id", f"persona_{idx+1}"),
                cluster_name=item.get("name", f"Segment {idx+1}"),
                feedback_samples=samples,
                pain_points=item.get("pains", []),
                emotions=item.get("emotions", [])
            )
            personas.append(p)

        return PersonaSummaryReport(
            total_customers_analyzed=total_samples,
            persona_count=len(personas),
            personas=personas
        )


if __name__ == "__main__":
    builder = PersonaBuilder()
    clusters = [
        {
            "id": "p_01",
            "name": "Efficiency Seekers",
            "samples": ["Too slow latency, need automated API integration for python pipeline", "Code integration takes long"],
            "pains": ["Slow Performance", "Lack of API docs"],
            "emotions": ["Frustration", "Disappointment"]
        }
    ]
    report = builder.build_persona_summary(clusters)
    print(report.model_dump_json(indent=2))
