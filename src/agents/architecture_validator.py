import json
from typing import Dict, Any
from pydantic import BaseModel


class ArchitectureValidator:
    def __init__(self):
        pass

    async def validate_plan(self, plan: Dict, inventory: Dict) -> Dict:
        # Validate that all local assets referenced exist in system inventory
        issues = []
        required_changes = []
        
        # Check if all referenced assets exist
        for asset in plan.get('local_assets_reused', []):
            found = False
            for model in inventory.get('models', []):
                if model['path'] == asset:
                    found = True
                    break
            
            if not found:
                issues.append(f"Referenced asset {asset} not found in system inventory")
                required_changes.append(f"Remove reference to {asset}")
        
        # Check module separation logic
        modules = plan.get('modules', [])
        if len(modules) < 2:
            issues.append("Insufficient module separation for proper architecture")
            required_changes.append("Add more modules for better separation of concerns")
        
        # Determine verdict
        if issues:
            return {
                'verdict': 'REJECTED',
                'domain': 'architecture',
                'issues': issues,
                'required_changes': required_changes,
                'confidence': 0.3
            }
        else:
            return {
                'verdict': 'APPROVED',
                'domain': 'architecture',
                'issues': [],
                'required_changes': [],
                'confidence': 0.9
            }