import asyncio
import aiohttp

from internal.probes import probe_http
from internal.reporter import report

class Engine:
    def __init__(self, config):
        config = config or {}
        
        self.interval = config.get("interval_seconds", 10)
        self.endpoints = config.get("endpoints", [])
        
        if not self.endpoints:
            print("Warning: No endpoints found in configuration. Please check config/endpoints.yaml")
            
        self._stop_event = asyncio.Event()
        
    def stop(self):
        """Triggers the engine to shut down gracefully"""
        self._stop_event.set()
        
    async def run(self):
        """Main loop for the monitoring engine"""
        async with aiohttp.ClientSession() as session:
            while not self._stop_event.is_set():
                await self._run_once(session)
                
                try:
                    await asyncio.wait_for(self._stop_event.wait(), timeout=self.interval)
                except asyncio.TimeoutError:
                    continue
                
    async def _run_once(self, session):
        """Executes all probes concurrently"""
        tasks = []
        for endpoint in self.endpoints:
            coro = probe_http(
                session, 
                endpoint.get("name", "Unknown"), 
                endpoint.get("url"), 
                endpoint.get("timeout_seconds", 5)
            )
            
            tasks.append(coro) 
            
        if not tasks:
            return

        results = await asyncio.gather(*tasks)
        
        for result in results:
            report(result)