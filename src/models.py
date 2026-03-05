from pydantic import BaseModel
from typing import List, Dict, Any


class SystemInventory(BaseModel):
    models: List[Dict]
    inference_servers: List[Dict]
    tools: List[Dict]
    active_ports: List[Dict]
    known_repos: List[Dict]

    class Config:
        extra = 'allow'

class RepoInfo(BaseModel):
    repo_name: str
    url: str
    description: str
    language: str
    topics: List[str]
    updated_at: str
    detected_at: str

    class Config:
        extra = 'allow'