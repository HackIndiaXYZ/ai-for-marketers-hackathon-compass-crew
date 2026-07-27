from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId


class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info=None):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_info, field):
        return {"type": "string"}


class AnalysisStatus(str, Enum):
    pending = "pending"
    processing = "processing"
    complete = "complete"
    failed = "failed"


class EmotionType(str, Enum):
    anger = "anger"
    frustration = "frustration"
    disappointment = "disappointment"
    anxiety = "anxiety"


class RevenuePotential(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"


class AdChannel(str, Enum):
    whatsapp = "whatsapp"
    google = "google"
    instagram = "instagram"
    email = "email"
    facebook = "facebook"
    landing_page = "landing_page"


class AdLanguage(str, Enum):
    english = "english"
    hinglish = "hinglish"
    hindi = "hindi"
    bengali = "bengali"


class CampaignStatus(str, Enum):
    draft = "draft"
    active = "active"
    paused = "paused"
    completed = "completed"


class UserModel(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    email: str
    hashed_password: str
    business_name: str = ""
    industry: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

    model_config = {"populate_by_name": True, "arbitrary_types_allowed": True}


class AnalysisModel(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    user_id: str
    topic: str
    industry: str
    status: AnalysisStatus = AnalysisStatus.pending
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    raw_data: str = ""
    progress: int = 0

    model_config = {"populate_by_name": True, "arbitrary_types_allowed": True}


class PainPointModel(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    analysis_id: str
    text: str
    frequency: int = 1
    emotion_score: float = Field(ge=0, le=10)
    emotion_type: EmotionType
    sources: list[str] = []
    rank: int = 0
    example_quotes: list[str] = []

    model_config = {"populate_by_name": True, "arbitrary_types_allowed": True}


class PersonaModel(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    analysis_id: str
    name: str
    age_range: str
    occupation: str
    pain_points: list[str] = []
    revenue_potential: RevenuePotential
    best_channels: list[str] = []
    language_preference: str = "hinglish"
    core_pain: str = ""
    emotional_state: str = ""
    what_they_want: str = ""

    model_config = {"populate_by_name": True, "arbitrary_types_allowed": True}


class AdAssetModel(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    analysis_id: str
    persona_id: str
    pain_point_id: str
    channel: AdChannel
    language: AdLanguage = AdLanguage.english
    content: str
    ctr_score: float = Field(ge=0, le=10, default=5.0)
    emotional_trigger: str = ""
    tone: str = ""

    model_config = {"populate_by_name": True, "arbitrary_types_allowed": True}


class CampaignModel(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    user_id: str
    analysis_id: str
    name: str
    status: CampaignStatus = CampaignStatus.draft
    total_budget: float = 0.0
    budget_split: dict = {}
    selected_channels: list[str] = []
    duration_days: int = 30
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True, "arbitrary_types_allowed": True}


class CompetitorModel(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    analysis_id: str
    competitor_name: str
    weaknesses: list[str] = []
    opportunity_ads: list[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True, "arbitrary_types_allowed": True}
