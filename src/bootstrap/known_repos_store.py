import json
import os
from typing import List, Dict


class KnownReposStore:
    def __init__(self):
        self.filename = 'known_repos.json'

    async def load_known_repos(self) -> List[Dict]:
        if not os.path.exists(self.filename):
            # Create empty file
            with open(self.filename, 'w') as f:
                json.dump([], f)
            return []
        
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading known repos: {e}")
            return []

    async def save_known_repos(self, repos: List[Dict]) -> None:
        with open(self.filename, 'w') as f:
            json.dump(repos, f, indent=2)

    async def add_repo(self, repo_info: Dict) -> None:
        repos = await self.load_known_repos()
        repos.append(repo_info)
        await self.save_known_repos(repos)