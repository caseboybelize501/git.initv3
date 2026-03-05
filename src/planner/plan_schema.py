from pydantic import BaseModel
from typing import List, Dict, Any


class PlanDocument(BaseModel):
    project_id: str
    repo_ref: str
    stack: List[str]
    modules: List[str]
    data_layer: str
    deployment_target: str
    local_assets_reused: List[str]
    ports_required: List[int]
    integration_points: List[str]
    validator_assignments: List[str]
    plan_rationale: str
    plan_status: str  # draft, approved, failed, deployed
    
    class Config:
        extra = 'allow'