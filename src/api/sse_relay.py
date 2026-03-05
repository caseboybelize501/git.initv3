import asyncio
import json
from typing import Dict, Any
from aiofiles import open as aopen


class SSERelay:
    def __init__(self):
        self.clients = set()

    async def add_client(self, response):
        self.clients.add(response)

    async def remove_client(self, response):
        self.clients.discard(response)

    async def broadcast(self, data: Dict[Any, Any]):
        message = f"data: {json.dumps(data)}\n\n"
        
        # Remove dead clients and send to live ones
        tasks = []
        for client in list(self.clients):
            try:
                await client.write(message)
                await client.flush()
            except Exception:
                self.clients.discard(client)

    async def send_event(self, event_type: str, data: Dict[Any, Any]):
        await self.broadcast({
            'type': event_type,
            'data': data
        })