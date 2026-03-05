import json
from typing import Dict, Any


class GateA:
    def __init__(self):
        pass

    async def check_permission(self, repo_info: Dict) -> Dict:
        # This would normally show GUI to user
        print(f"\nGate A - Repository Permission Required")
        print(f"Repository: {repo_info['repo_name']}")
        print(f"Description: {repo_info['description']}")
        
        # Show system inventory summary
        try:
            with open('SystemInventory.json', 'r') as f:
                inventory = json.load(f)
                
                models_count = len(inventory.get('models', []))
                servers_count = len(inventory.get('inference_servers', []))
                tools_count = len(inventory.get('tools', []))
                
                print(f"\nSystem Inventory Summary:")
                print(f"  Models: {models_count}")
                print(f"  Inference Servers: {servers_count}")
                print(f"  Tools Available: {tools_count}")
        except Exception as e:
            print(f"Error reading system inventory: {e}")
        
        # Simulate user approval (in real implementation, this would be GUI)
        action = input("\nApprove or Skip? (approve/skip): ").lower()
        
        return {
            'repo_name': repo_info['repo_name'],
            'action': action,
            'approved': action == 'approve'
        }