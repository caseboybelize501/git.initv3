import json
from typing import Dict, Any


class SecurityValidator:
    def __init__(self):
        pass

    async def validate_plan(self, plan: Dict, inventory: Dict) -> Dict:
        issues = []
        required_changes = []
        
        # Check for secret storage in repo
        if 'secrets' in plan.get('modules', []):
            issues.append("Secrets found in modules - this is a security risk")
            required_changes.append("Remove secrets from repository and use secure environment variables")
        
        # Check for sensitive data routing
        if plan.get('data_layer') == 'shared_free_tier':
            issues.append("Routing sensitive data through shared free-tier infrastructure without encryption")
            required_changes.append("Use encrypted storage or move to dedicated infrastructure")
        
        # Check dependency choices (simplified)
        stack = plan.get('stack', [])
        if 'django' in stack and 'djangorestframework' not in stack:
            issues.append("Missing DRF for proper API security handling")
            required_changes.append("Add Django REST Framework for better API security")
        
        # Determine verdict
        if issues:
            return {
                'verdict': 'REJECTED',
                'domain': 'security',
                'issues': issues,
                'required_changes': required_changes,
                'confidence': 0.5
            }
        else:
            return {
                'verdict': 'APPROVED',
                'domain': 'security',
                'issues': [],
                'required_changes': [],
                'confidence': 0.9
            }