import json
from typing import Dict, Any
from src.planner.host_matrix import get_host_matrix


class DeploymentValidator:
    def __init__(self):
        self.host_matrix = get_host_matrix()

    async def validate_plan(self, plan: Dict, inventory: Dict) -> Dict:
        issues = []
        required_changes = []
        
        # Check if deployment target is free-tier
        target = plan.get('deployment_target')
        if not target or target not in self.host_matrix:
            issues.append("Invalid or non-free-tier deployment target selected")
            required_changes.append("Select a valid free-tier host from the matrix")
        else:
            # Check if host is actually free
            host_info = self.host_matrix[target]
            if not host_info.get('free', True):
                issues.append(f"Selected host {target} is not free tier")
                required_changes.append("Select a free-tier host from the matrix")
        
        # Check port conflicts
        ports_required = plan.get('ports_required', [])
        active_ports = [p['port'] for p in inventory.get('active_ports', [])]
        
        for port in ports_required:
            if port in active_ports:
                issues.append(f"Port {port} is already in use")
                required_changes.append(f"Change required port to avoid conflict with existing service")
        
        # Determine verdict
        if issues:
            return {
                'verdict': 'REJECTED',
                'domain': 'deployment',
                'issues': issues,
                'required_changes': required_changes,
                'confidence': 0.4
            }
        else:
            return {
                'verdict': 'APPROVED',
                'domain': 'deployment',
                'issues': [],
                'required_changes': [],
                'confidence': 0.8
            }