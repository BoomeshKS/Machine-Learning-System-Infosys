from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Project, RiskAssessment, SwotAnalysis, FeasibilityAssessment
from app.schemas import RiskInput, RiskOut, SwotOut, FeasibilityOut
from app.services.risk_engine import calculate_risk
from app.services.swot_service import generate_swot

router = APIRouter(tags=["Milestone 2 – Risk, SWOT & Feasibility"])

def require_project(db: Session, project_id: int) -> Project:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.post("/projects/{project_id}/risk-assessment", response_model=RiskOut, status_code=201)
def create_risk_assessment(project_id: int, payload: RiskInput, db: Session = Depends(get_db)):
    require_project(db, project_id)
    result = calculate_risk(payload)
    assessment = RiskAssessment(project_id=project_id, **result)
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    return assessment

@router.get("/projects/{project_id}/risk-assessment", response_model=RiskOut)
def get_latest_risk_assessment(project_id: int, db: Session = Depends(get_db)):
    require_project(db, project_id)
    result = (db.query(RiskAssessment)
              .filter(RiskAssessment.project_id == project_id)
              .order_by(RiskAssessment.created_at.desc(), RiskAssessment.id.desc())
              .first())
    if not result:
        raise HTTPException(status_code=404, detail="No risk assessment found")
    return result

@router.post("/projects/{project_id}/swot", response_model=SwotOut, status_code=201)
def create_swot(project_id: int, db: Session = Depends(get_db)):
    project = require_project(db, project_id)
    result = generate_swot(project)
    analysis = SwotAnalysis(project_id=project_id, **result)
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis

@router.get("/projects/{project_id}/swot", response_model=SwotOut)
def get_latest_swot(project_id: int, db: Session = Depends(get_db)):
    require_project(db, project_id)
    result = (db.query(SwotAnalysis)
              .filter(SwotAnalysis.project_id == project_id)
              .order_by(SwotAnalysis.created_at.desc(), SwotAnalysis.id.desc())
              .first())
    if not result:
        raise HTTPException(status_code=404, detail="No SWOT analysis found")
    return result

@router.post("/projects/{project_id}/feasibility", response_model=FeasibilityOut, status_code=201)
def create_feasibility(project_id: int, db: Session = Depends(get_db)):
    require_project(db, project_id)
    risk = (db.query(RiskAssessment)
            .filter(RiskAssessment.project_id == project_id)
            .order_by(RiskAssessment.created_at.desc(), RiskAssessment.id.desc())
            .first())
    if not risk:
        raise HTTPException(status_code=400, detail="Run risk assessment before feasibility assessment")

    score = round(100 - risk.overall_risk_score, 2)
    level = "High" if score >= 70 else "Moderate" if score >= 40 else "Low"
    explanation = (
        f"Feasibility score is derived as 100 minus the overall risk score. "
        f"The current risk level is {risk.risk_level}. This is a rule-based screening "
        f"indicator, not a complete technical, financial, legal, or market feasibility study."
    )
    item = FeasibilityAssessment(
        project_id=project_id,
        risk_assessment_id=risk.id,
        feasibility_score=score,
        feasibility_level=level,
        explanation=explanation,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.get("/projects/{project_id}/feasibility", response_model=FeasibilityOut)
def get_latest_feasibility(project_id: int, db: Session = Depends(get_db)):
    require_project(db, project_id)
    result = (db.query(FeasibilityAssessment)
              .filter(FeasibilityAssessment.project_id == project_id)
              .order_by(FeasibilityAssessment.created_at.desc(), FeasibilityAssessment.id.desc())
              .first())
    if not result:
        raise HTTPException(status_code=404, detail="No feasibility assessment found")
    return result
