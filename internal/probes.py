import asyncio
import aiohttp

async def probe_http(session, name, url, timeout):
    start = asyncio.get_event_loop().time()
    try:
        async with session.get(url, timeout = timeout) as response:
            latency = (asyncio.get_event_loop().time() - start) * 1000
            
            return {"service": name, "url": url, "status": "ok" if response.status < 400 else "http_error", "http_status": response.status, "latency_ms": round(latency, 2)}
    except asyncio.TimeoutError:
        return {"service": name, "url": url, "status": "timeout"}
    except aiohttp.ClientConnectionError:
        return {"service": name, "url": url, "status": "connection_error"}
    except Exception as e:
        return {"service":name , "url": url, "status":"unknown_error", "error": str(e)}