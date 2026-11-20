from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Project
from app.schemas import ProjectCreate, ProjectOut

router = APIRouter(tags=["Projects"])

@router.post("/projects", response_model=ProjectOut, status_code=201)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    project = Project(**payload.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.get("/projects", response_model=list[ProjectOut])
def list_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if limit < 1 or limit > 500:
        raise HTTPException(status_code=400, detail="limit must be between 1 and 500")
    return db.query(Project).order_by(Project.created_at.desc()).offset(skip).limit(limit).all()

@router.get("/projects/{project_id}", response_model=ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project