import os
import hashlib
from pathlib import Path
from typing import List, Dict


class ModelScanner:
    def __init__(self):
        self.model_extensions = {'.gguf', '.ggml', '.safetensors', '.bin', '.onnx', '.pt', '.pth'}

    async def scan_models(self) -> List[Dict]:
        models = []
        
        # Scan C: and D:
        drives = ['C:', 'D:']
        for drive in drives:
            if os.path.exists(drive):
                for root, dirs, files in os.walk(drive):
                    for file in files:
                        if any(file.endswith(ext) for ext in self.model_extensions):
                            file_path = os.path.join(root, file)
                            file_size = os.path.getsize(file_path)
                            
                            # Only include files > 100MB
                            if file_size > 100 * 1024 * 1024:
                                model_info = self._get_model_info(file_path, file_size)
                                models.append(model_info)
        
        # Deduplicate by SHA256 hash
        unique_models = self._deduplicate_models(models)
        return unique_models

    def _get_model_info(self, path: str, size: int) -> Dict:
        # Calculate SHA256 of first 4KB + file size
        with open(path, 'rb') as f:
            first_4kb = f.read(4096)
            hash_input = first_4kb + str(size).encode()
            sha256_hash = hashlib.sha256(hash_input).hexdigest()
        
        # Get file extension
        ext = os.path.splitext(path)[1]
        
        return {
            'hash': sha256_hash,
            'path': path,
            'size_gb': round(size / (1024**3), 2),
            'format': ext,
            'detected_at': self._get_timestamp()
        }

    def _deduplicate_models(self, models: List[Dict]) -> List[Dict]:
        seen_hashes = set()
        unique_models = []
        
        for model in models:
            if model['hash'] not in seen_hashes:
                seen_hashes.add(model['hash'])
                unique_models.append(model)
        
        return unique_models

    def _get_timestamp(self) -> str:
        import datetime
        return datetime.datetime.now().isoformat()