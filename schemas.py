

class ProjectCreate(BaseModel):

    project_name: str

    project_type: str

    industry: str

    business_model: Optional[str] = None

    target_market: Optional[str] = None

    budget: Optional[float] = Float(default=0.0, ge=0.0)

    description: str

    objectives: str

    competitors: Optional[str] = None


    
