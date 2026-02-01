import yaml
import asyncio
import signal
from internal.engine import Engine

# i have  to load the yaml file
# starting the async engine

def load_config():
    with open("config/endpoints.yaml", "r") as file:
        return yaml.safe_load(file)
    
async def main():
    config = load_config()
    engine = Engine(config)
    
    loop = asyncio.get_running_loop()
    
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig , engine.stop)
        
    await engine.run()
    
if __name__ == "__main__":
    asyncio.run(main())