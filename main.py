from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy.orm import Session

from database import Base, engine, get_db

from models import Project, MarketAnalysis

from schemas import ProjectCreate

from gemini_service import generate_market_analysis


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Failure Prediction AI",
    description="Milestone 1 - Data Collection and Market Intelligence",
    version="1.0.0"
)


@app.get("/")
def home():

    return {
        "message": "Failure Prediction AI Backend Running"
    }


# TARGET 1: PROJECT SUBMISSION


@app.post("/projects")
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):

    new_project = Project(
        **project.model_dump()
    )

    db.add(new_project)

    db.commit()

    db.refresh(new_project)

    return {
        "message": "Project submitted successfully",
        "project_id": new_project.id,
        "project_name": new_project.project_name
    }


# TARGET 2: MARKET INTELLIGENCE


@app.post("/projects/{project_id}/market-analysis")
def analyse_market(
    project_id: int,
    db: Session = Depends(get_db)
):

    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if not project:

        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    try:

        analysis = generate_market_analysis(project)

    except Exception as e:

        raise HTTPException(
            status_code=502,
            detail=f"AI analysis failed: {str(e)}"
        )

    # TARGET 3: STORE ANALYSIS IN POSTGRESQL

    market_result = MarketAnalysis(

        project_id=project.id,

        market_overview=analysis["market_overview"],

        target_customers=analysis["target_customers"],

        market_opportunities=analysis["market_opportunities"],

        market_challenges=analysis["market_challenges"],

        competitors=analysis["competitors"],

        industry_trends=analysis["industry_trends"]

    )

    db.add(market_result)

    db.commit()

    db.refresh(market_result)

    return {

        "message": "Market analysis completed",

        "project_id": project.id,

        "analysis": analysis

    }


# GET ALL PROJECTS


@app.get("/projects")
def get_projects(
    db: Session = Depends(get_db)
):

    projects = db.query(Project).all()

    return projects


# GET PROJECT DETAILS


@app.get("/projects/{project_id}")
def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):

    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if not project:

        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return project


# GET SAVED MARKET ANALYSIS


@app.get("/projects/{project_id}/market-analysis")
def get_market_analysis(
    project_id: int,
    db: Session = Depends(get_db)
):

    results = db.query(MarketAnalysis).filter(
        MarketAnalysis.project_id == project_id
    ).all()

    return results