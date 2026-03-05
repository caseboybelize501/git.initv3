import asyncio
import logging
from src.bootstrap.system_scanner import SystemScanner
from src.agents.watcher_agent import WatcherAgent
from src.routing.event_bus import EventBus

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    # Initialize system scanner
    scanner = SystemScanner()
    await scanner.scan()
    
    # Initialize event bus
    event_bus = EventBus()
    
    # Initialize watcher agent
    watcher = WatcherAgent(event_bus)
    
    # Start watching loop
    logger.info("Starting GitHub watcher...")
    await watcher.start_watching()
    
    # Keep running
    try:
        while True:
            await asyncio.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        logger.info("Shutting down...")

if __name__ == "__main__":
    asyncio.run(main())