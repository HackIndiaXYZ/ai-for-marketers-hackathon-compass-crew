from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


# ── Auth Schemas ──────────────────────────────────────────

class RegisterRequest(BaseModel):
    email: str
    password: str
    business_name: str = ""
    industry: str = ""


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: "UserResponse"


class UserResponse(BaseModel):
    id: str
    email: str
    business_name: str
    industry: str
    created_at: datetime
    is_active: bool


# ── Analysis Schemas ──────────────────────────────────────

class AnalysisCreateRequest(BaseModel):
    topic: str
    industry: str
    language: str = "hinglish"


class AnalysisResponse(BaseModel):
    id: str
    user_id: str
    topic: str
    industry: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    progress: int = 0


class AnalysisStatusResponse(BaseModel):
    id: str
    status: str
    progress: int
    topic: str
    created_at: datetime


# ── Pain Points Schemas ───────────────────────────────────

class PainPointResponse(BaseModel):
    id: str
    analysis_id: str
    text: str
    frequency: int
    emotion_score: float
    emotion_type: str
    sources: list[str]
    rank: int
    example_quotes: list[str]


class PainPointListResponse(BaseModel):
    pain_points: list[PainPointResponse]
    insight_narrative: str
    total_count: int


# ── Personas Schemas ──────────────────────────────────────

class PersonaResponse(BaseModel):
    id: str
    analysis_id: str
    name: str
    age_range: str
    occupation: str
    pain_points: list[str]
    revenue_potential: str
    best_channels: list[str]
    language_preference: str
    core_pain: str
    emotional_state: str
    what_they_want: str


class PersonaListResponse(BaseModel):
    personas: list[PersonaResponse]
    total_count: int


# ── Ad Assets Schemas ─────────────────────────────────────

class AdAssetResponse(BaseModel):
    id: str
    analysis_id: str
    persona_id: str
    pain_point_id: str
    channel: str
    language: str
    content: str
    ctr_score: float
    emotional_trigger: str
    tone: str


class AdAssetPackResponse(BaseModel):
    persona_id: str
    persona_name: str
    pain_point: str
    ads: list[AdAssetResponse]


# ── Campaign Schemas ──────────────────────────────────────

class CampaignCreateRequest(BaseModel):
    analysis_id: str
    name: str
    total_budget: float
    selected_channels: list[str] = []
    duration_days: int = 30


class CampaignResponse(BaseModel):
    id: str
    user_id: str
    analysis_id: str
    name: str
    status: str
    total_budget: float
    budget_split: dict
    selected_channels: list[str]
    duration_days: int
    created_at: datetime


# ── Optimizer Schemas ─────────────────────────────────────

class OptimizerRequest(BaseModel):
    analysis_id: str
    budget: float


class OptimizerResponse(BaseModel):
    variant_scores: list[dict]
    budget_split: dict
    projected_ctr: float
    projected_conversions: int
    roi_estimate: float
    narrative: str


# ── Insights Schemas ──────────────────────────────────────

class InsightResponse(BaseModel):
    analysis_id: str
    narrative: str
    top_pain: str
    best_persona: str
    recommended_channel: str
    competitor_gap: str


# ── Competitor Schemas ────────────────────────────────────

class CompetitorRequest(BaseModel):
    analysis_id: str
    competitor_name: str


class CompetitorResponse(BaseModel):
    id: str
    analysis_id: str
    competitor_name: str
    weaknesses: list[str]
    opportunity_ads: list[str]
    created_at: datetime


# ── Trends Schemas ────────────────────────────────────────

class TrendResponse(BaseModel):
    analysis_id: str
    trending_pains: list[dict]
    seasonal_insight: str
    opportunity_scores: dict


class SeasonalRequest(BaseModel):
    industry: str
    festival_or_season: str
    pain_points: list[str] = []


# ── Simulator Schemas ─────────────────────────────────────

class SimulatorRequest(BaseModel):
    analysis_id: str
    budget: float
    duration_days: int
    selected_channels: list[str]


class SimulatorResponse(BaseModel):
    analysis_id: str
    daily_projection: dict
    total_conversions: int
    total_revenue: float
    roi_percentage: float
    best_performing_day: int
    recommended_variant: str
    confidence_level: str


# ── Export Schemas ─────────────────────────────────────────

class ExportRequest(BaseModel):
    analysis_id: str
    format: str = "json"


class ExportResponse(BaseModel):
    download_url: Optional[str] = None
    content: Optional[str] = None
    format: str
    filename: str
