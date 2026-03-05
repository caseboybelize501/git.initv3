import subprocess
import re
from typing import List, Dict


class ToolScanner:
    def __init__(self):
        self.tools = ['node', 'python3', 'git', 'docker', 'pnpm', 'bun', 'npm', 'cargo', 'go']

    async def scan_tools(self) -> List[Dict]:
        tools = []
        
        for tool in self.tools:
            try:
                # Check if tool is in PATH
                result = subprocess.run(['which', tool], capture_output=True, text=True)
                path = result.stdout.strip() if result.returncode == 0 else None
                
                # Get version
                version_result = subprocess.run([tool, '--version'], capture_output=True, text=True)
                version = version_result.stdout.strip() if version_result.returncode == 0 else 'unknown'
                
                tool_info = {
                    'tool': tool,
                    'version': version,
                    'path': path,
                    'in_path': path is not None
                }
                tools.append(tool_info)
            except Exception as e:
                # Tool not found or error occurred
                tool_info = {
                    'tool': tool,
                    'version': 'unknown',
                    'path': None,
                    'in_path': False
                }
                tools.append(tool_info)
        
        return tools