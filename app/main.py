from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import projects, milestone2

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Failure Prediction AI – Startup & Project Risk Analyzer",
    description="Milestone 1 project submission plus Milestone 2 risk, SWOT and feasibility APIs.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects.router, prefix="/api")
app.include_router(milestone2.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Failure Prediction AI API is running", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok"}
