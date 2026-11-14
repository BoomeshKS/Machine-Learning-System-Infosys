from sqlalchemy import (
    Column, Integer, String,
    Text, Float, ForeignKey,
    JSON, DateTime
)
from sqlalchemy.sql import func

from database import Base


class Project(Base):

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)

    project_name = Column(String(200), nullable=False)

    project_type = Column(String(100))

    industry = Column(String(150))

    business_model = Column(String(100))

    target_market = Column(Text)

    budget = Column(Float)

    description = Column(Text)

    objectives = Column(Text)

    competitors = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


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