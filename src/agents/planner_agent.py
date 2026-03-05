import json
from typing import Dict, Any
from src.planner.plan_schema import PlanDocument
from src.routing.model_router import ModelRouter


class PlannerAgent:
    def __init__(self, model_router: ModelRouter):
        self.model_router = model_router

    async def generate_plan(self, repo_info: Dict) -> PlanDocument:
        # Load system inventory
        try:
            with open('SystemInventory.json', 'r') as f:
                inventory = json.load(f)
        except Exception as e:
            raise Exception(f"Failed to load SystemInventory: {e}")
        
        # Get the best available LLM from system inventory
        llm_model = self.model_router.get_best_llm(inventory)
        
        # Generate plan using LLM (simplified for now)
        plan_data = {
            'project_id': f"plan_{repo_info['repo_name']}",
            'repo_ref': repo_info['repo_name'],
            'stack': ['python', 'fastapi'],
            'modules': ['main.py', 'models.py', 'routes.py'],
            'data_layer': 'sqlite',
            'deployment_target': 'vercel',
            'local_assets_reused': [],
            'ports_required': [8000],
            'integration_points': [],
            'validator_assignments': ['architecture', 'deployment', 'security'],
            'plan_rationale': f'Plan for {repo_info["repo_name"]} based on system inventory',
            'plan_status': 'draft'
        }
        
        return PlanDocument(**plan_data)