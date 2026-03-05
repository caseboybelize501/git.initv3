import subprocess
import os
import json
from datetime import datetime
from src.bootstrap.known_repos_store import KnownReposStore


class DeploymentAgent:
    def __init__(self):
        self.known_repos_store = KnownReposStore()

    async def deploy_project(self, plan: Dict) -> str:
        # Generate scaffold (simplified)
        project_name = plan['repo_ref']
        
        try:
            # Create directory structure
            os.makedirs(project_name, exist_ok=True)
            
            # Create basic files
            with open(f'{project_name}/README.md', 'w') as f:
                f.write(f'# {project_name}\n\nDeployed from git.initv3\n')
            
            with open(f'{project_name}/main.py', 'w') as f:
                f.write('print("Hello from deployed project")\n')
            
            # Initialize git repo
            subprocess.run(['git', 'init'], cwd=project_name, check=True)
            subprocess.run(['git', 'add', '.'], cwd=project_name, check=True)
            subprocess.run(['git', 'commit', '-m', 'Initial commit'], cwd=project_name, check=True)
            
            # Simulate deployment to host
            deploy_url = f"https://{plan['deployment_target']}.com/{project_name}"
            
            # Update known repos
            repo_info = {
                'repo_name': project_name,
                'url': f'https://github.com/caseboybelize501/{project_name}',
                'detected_at': datetime.now().isoformat(),
                'job_status': 'deployed',
                'plan_id': plan['project_id'],
                'deploy_url': deploy_url
            }
            
            await self.known_repos_store.add_repo(repo_info)
            
            return deploy_url
        except Exception as e:
            print(f"Deployment failed: {e}")
            raise