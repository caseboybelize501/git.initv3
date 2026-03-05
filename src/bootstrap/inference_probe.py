import httpx
import asyncio
from typing import List, Dict
import json


class InferenceProbe:
    def __init__(self):
        self.ports = [11434, 8000, 1234, 8080, 5000]
        self.timeout = 5

    async def probe_servers(self) -> List[Dict]:
        servers = []
        
        for port in self.ports:
            try:
                # Try Ollama API endpoint
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.get(f'http://localhost:{port}/api/tags')
                    if response.status_code == 200:
                        server_info = {
                            'port': port,
                            'provider': 'Ollama',
                            'models': response.json().get('models', []),
                            'response_ms': response.elapsed.total_seconds() * 1000,
                            'alive': True
                        }
                        servers.append(server_info)
                        continue
                
                # Try OpenAI-compatible endpoint
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.get(f'http://localhost:{port}/v1/models')
                    if response.status_code == 200:
                        server_info = {
                            'port': port,
                            'provider': 'OpenAI-compatible',
                            'models': response.json().get('data', []),
                            'response_ms': response.elapsed.total_seconds() * 1000,
                            'alive': True
                        }
                        servers.append(server_info)
                        continue
            except Exception as e:
                # Port not responding or not accessible
                pass
        
        return servers