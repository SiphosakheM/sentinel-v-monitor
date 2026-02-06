import asyncio
import aiohttp

from internal.probes import probe_http
from internal.reporter import report

class Engine:
    def __init__(self, config):
        self.interval = config.get("interval_seconds", 10)
        self.endpoints = config["endpoints"]
        self._stop_event = asyncio.Event()
        
    def stop(self):
        self._stop_event.set()
        
    async def run(self):
        async with aiohttp.ClientSession() as session:
            while not self._stop_event.is_set():
                await self._run_once(session)
                try:
                    await asyncio.wait_for(self._stop_event.wait(), timeout=self.interval)
                except asyncio.TimeoutError:
                    continue
                
    async def _run_once(self, session):
        tasks = []
        for endpoint in self.endpoints:
            coro = probe_http(
                session, 
                endpoint["name"], 
                endpoint["url"], 
                endpoint.get("timeout_seconds", 5)
            )
            tasks.append(coro)
            

        results = await asyncio.gather(*tasks)
        
        for result in results:
            report(result)