from datetime import datetime
from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON, String, Text, Column, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base




class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_name: Mapped[str] = mapped_column(String(200), nullable=False)
    project_type: Mapped[str] = mapped_column(String(80), default="startup")
    industry_sector: Mapped[str | None] = mapped_column(String(120), nullable=True)
    business_model: Mapped[str | None] = mapped_column(String(120), nullable=True)
    budget: Mapped[float | None] = mapped_column(Float, nullable=True)
    target_market: Mapped[str | None] = mapped_column(String(200), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    risk_assessments: Mapped[list["RiskAssessment"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    swot_analyses: Mapped[list["SwotAnalysis"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    feasibility_assessments: Mapped[list["FeasibilityAssessment"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )


class RiskAssessment(Base):
    __tablename__ = "risk_assessments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    financial_risk: Mapped[float] = mapped_column(Float)
    market_risk: Mapped[float] = mapped_column(Float)
    technical_risk: Mapped[float] = mapped_column(Float)
    operational_risk: Mapped[float] = mapped_column(Float)
    competition_regulatory_risk: Mapped[float] = mapped_column(Float)
    overall_risk_score: Mapped[float] = mapped_column(Float)
    risk_level: Mapped[str] = mapped_column(String(20))
    success_probability_indicator: Mapped[float] = mapped_column(Float)
    input_data: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    project: Mapped["Project"] = relationship(back_populates="risk_assessments")

class SwotAnalysis(Base):
    __tablename__ = "swot_analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    strengths: Mapped[list] = mapped_column(JSON)
    weaknesses: Mapped[list] = mapped_column(JSON)
    opportunities: Mapped[list] = mapped_column(JSON)
    threats: Mapped[list] = mapped_column(JSON)
    provider: Mapped[str] = mapped_column(String(30), default="rules")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    project: Mapped["Project"] = relationship(back_populates="swot_analyses")

class FeasibilityAssessment(Base):
    __tablename__ = "feasibility_assessments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    risk_assessment_id: Mapped[int] = mapped_column(ForeignKey("risk_assessments.id"))
    feasibility_score: Mapped[float] = mapped_column(Float)
    feasibility_level: Mapped[str] = mapped_column(String(30))
    explanation: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)



class MarketAnalysis(Base):

    __tablename__ = "market_analysis"

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(
        Integer,
        ForeignKey("projects.id")
    )

    market_overview = Column(Text)

    target_customers = Column(Text)

    market_opportunities = Column(JSON)

    market_challenges = Column(JSON)

    competitors = Column(JSON)

    industry_trends = Column(JSON)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )