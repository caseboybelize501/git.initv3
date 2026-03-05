import os
import json
import hashlib
import subprocess
from pathlib import Path
from src.bootstrap.model_scanner import ModelScanner
from src.bootstrap.inference_probe import InferenceProbe
from src.bootstrap.tool_scanner import ToolScanner
from src.bootstrap.port_registry import PortRegistry
from src.bootstrap.known_repos_store import KnownReposStore
from src.models import SystemInventory


class SystemScanner:
    def __init__(self):
        self.model_scanner = ModelScanner()
        self.inference_probe = InferenceProbe()
        self.tool_scanner = ToolScanner()
        self.port_registry = PortRegistry()
        self.known_repos_store = KnownReposStore()

    async def scan(self):
        print("Starting system scan...")
        
        # Phase 1: Model inventory
        models = await self.model_scanner.scan_models()
        print(f"Found {len(models)} models")
        
        # Phase 2: Inference server probe
        servers = await self.inference_probe.probe_servers()
        print(f"Found {len(servers)} inference servers")
        
        # Phase 3: Tool inventory
        tools = await self.tool_scanner.scan_tools()
        print(f"Found {len(tools)} tools")
        
        # Phase 4: Port registry
        ports = await self.port_registry.get_active_ports()
        print(f"Found {len(ports)} active ports")
        
        # Phase 5: Known repos register
        known_repos = await self.known_repos_store.load_known_repos()
        
        # Create system inventory object
        inventory = SystemInventory(
            models=models,
            inference_servers=servers,
            tools=tools,
            active_ports=ports,
            known_repos=known_repos
        )
        
        # Write to file
        with open('SystemInventory.json', 'w') as f:
            json.dump(inventory.dict(), f, indent=2)
        
        print("System scan completed and inventory written")
        return inventory