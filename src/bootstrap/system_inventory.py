import json
from typing import List, Dict
from pydantic import BaseModel


class SystemInventory(BaseModel):
    models: List[Dict]
    inference_servers: List[Dict]
    tools: List[Dict]
    active_ports: List[Dict]
    known_repos: List[Dict]

    class Config:
        # Allow extra fields for flexibility
        extra = 'allow'

async def validate_inventory(inventory: SystemInventory) -> bool:
    # Basic validation checks
    try:
        # Check that all required fields exist
        assert inventory.models is not None
        assert inventory.inference_servers is not None
        assert inventory.tools is not None
        assert inventory.active_ports is not None
        assert inventory.known_repos is not None
        
        print("System inventory validation passed")
        return True
    except Exception as e:
        print(f"System inventory validation failed: {e}")
        return False