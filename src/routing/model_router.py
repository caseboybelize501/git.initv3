import json
from typing import Dict, Any


class ModelRouter:
    def __init__(self):
        pass

    async def get_best_llm(self, inventory: Dict) -> str:
        # Find best available LLM from system inventory
        
        # Check for inference servers first
        servers = inventory.get('inference_servers', [])
        if servers:
            # Prefer Ollama servers
            ollama_server = next((s for s in servers if s['provider'] == 'Ollama'), None)
            if ollama_server:
                return f"ollama:{ollama_server['port']}"
            
            # Fallback to first available server
            return f"http://localhost:{servers[0]['port']}"
        
        # No inference servers found - use default
        return "default_llm"

    async def get_model_for_validator(self, validator_name: str, inventory: Dict) -> str:
        # Return appropriate model based on validator type
        if validator_name == 'architecture':
            return self._get_best_model(inventory, ['llama3', 'gemma', 'mistral'])
        elif validator_name == 'deployment':
            return self._get_best_model(inventory, ['llama3', 'gemma', 'mistral'])
        elif validator_name == 'security':
            return self._get_best_model(inventory, ['llama3', 'gemma', 'mistral'])
        
        return "default_model"

    def _get_best_model(self, inventory: Dict, preferred_models: List[str]) -> str:
        # Find best model from system inventory
        models = inventory.get('models', [])
        
        # Try to find preferred models first
        for model in models:
            model_path = model['path']
            if any(preference in model_path.lower() for preference in preferred_models):
                return model_path
        
        # Fallback to first available model
        if models:
            return models[0]['path']
        
        return "default_model"