import json
import os
from typing import Dict, Any
from src.planner.plan_schema import PlanDocument


class PlanStore:
    def __init__(self):
        self.plans_dir = 'plans'
        os.makedirs(self.plans_dir, exist_ok=True)

    async def save_plan(self, plan: PlanDocument) -> None:
        filename = f"{self.plans_dir}/{plan.project_id}.json"
        with open(filename, 'w') as f:
            json.dump(plan.dict(), f, indent=2)

    async def load_plan(self, project_id: str) -> PlanDocument:
        filename = f"{self.plans_dir}/{project_id}.json"
        with open(filename, 'r') as f:
            data = json.load(f)
        return PlanDocument(**data)