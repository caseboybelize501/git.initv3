import json
from typing import Dict, Any


class GateB:
    def __init__(self):
        pass

    async def check_permission(self, plan: Dict) -> Dict:
        # This would normally show GUI to user
        print(f"\nGate B - Deployment Permission Required")
        print(f"Plan ID: {plan['project_id']}")
        print(f"Deployment Target: {plan['deployment_target']}")
        
        # Show plan details
        print(f"\nSelected Stack: {', '.join(plan.get('stack', []))}")
        print(f"Modules: {', '.join(plan.get('modules', []))}")
        print(f"Ports Required: {plan.get('ports_required', [])}")
        
        # Show local assets reused
        assets = plan.get('local_assets_reused', [])
        if assets:
            print(f"\nAssets Reused from System Inventory:")
            for asset in assets:
                print(f"  - {asset}")
        else:
            print("\nNo local assets reused")
        
        # Simulate user approval (in real implementation, this would be GUI)
        action = input("\nApprove or Cancel? (approve/cancel): ").lower()
        
        return {
            'project_id': plan['project_id'],
            'action': action,
            'approved': action == 'approve'
        }