import asyncio
import httpx
import json
from datetime import datetime
from src.bootstrap.known_repos_store import KnownReposStore
from src.routing.event_bus import EventBus


class WatcherAgent:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.known_repos_store = KnownReposStore()
        self.github_api_url = "https://api.github.com"
        self.username = "caseboybelize501"
        self.interval = 60  # seconds

    async def start_watching(self):
        while True:
            await self.check_repositories()
            await asyncio.sleep(self.interval)

    async def check_repositories(self):
        try:
            # Get repositories from GitHub API
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.github_api_url}/users/{self.username}/repos",
                    params={
                        "per_page": 100,
                        "sort": "updated"
                    }
                )
                
                if response.status_code == 200:
                    repos = response.json()
                    known_repos = await self.known_repos_store.load_known_repos()
                    
                    # Check for new repositories
                    for repo in repos:
                        repo_name = repo['name']
                        repo_url = repo['html_url']
                        
                        # Check if already processed
                        existing_repo = next((r for r in known_repos if r['repo_name'] == repo_name), None)
                        
                        if not existing_repo:
                            # New repository detected
                            print(f"New repository detected: {repo_name}")
                            
                            # Emit event
                            await self.event_bus.emit('repo_detected', {
                                'repo_name': repo_name,
                                'url': repo_url,
                                'description': repo.get('description', ''),
                                'language': repo.get('language', ''),
                                'topics': repo.get('topics', []),
                                'updated_at': repo['updated_at'],
                                'detected_at': datetime.now().isoformat()
                            })
                else:
                    print(f"Failed to fetch repositories: {response.status_code}")
        except Exception as e:
            print(f"Error checking repositories: {e}")