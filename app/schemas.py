from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class ProjectCreate(BaseModel):
    project_name: str = Field(min_length=2, max_length=200)
    project_type: str = "startup"
    industry_sector: Optional[str] = None
    business_model: Optional[str] = None
    budget: Optional[float] = Field(default=None, ge=0)
    target_market: Optional[str] = None
    description: str = Field(min_length=10)

class ProjectOut(ProjectCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class RiskInput(BaseModel):
    # Ratings 1–5. For adequacy/readiness/experience/availability/validation:
    # 1 = very poor and 5 = excellent. Competition/regulatory: 1 = low, 5 = very high.
    budget_adequacy: int = Field(ge=1, le=5)
    market_validation: int = Field(ge=1, le=5)
    technical_readiness: int = Field(ge=1, le=5)
    team_experience: int = Field(ge=1, le=5)
    resource_availability: int = Field(ge=1, le=5)
    competition_intensity: int = Field(ge=1, le=5)
    regulatory_complexity: int = Field(ge=1, le=5)

class RiskOut(BaseModel):
    id: int
    project_id: int
    financial_risk: float
    market_risk: float
    technical_risk: float
    operational_risk: float
    competition_regulatory_risk: float
    overall_risk_score: float
    risk_level: str
    success_probability_indicator: float
    input_data: dict
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class SwotOut(BaseModel):
    id: int
    project_id: int
    strengths: list[str]
    weaknesses: list[str]
    opportunities: list[str]
    threats: list[str]
    provider: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class FeasibilityOut(BaseModel):
    id: int
    project_id: int
    risk_assessment_id: int
    feasibility_score: float
    feasibility_level: str
    explanation: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
