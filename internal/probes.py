import asyncio
import aiohttp
import ssl
import socket
from datetime import datetime
from cryptography import x509

def get_ssl_expiry(hostname):
    """Sync helper to grab SSL expiry date."""
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443), timeout=3) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert_bin = ssock.getpeercert(binary_form=True)
            cert = x509.load_der_x509_certificate(cert_bin)
            return cert.not_valid_after_utc

async def probe_http(session, name, url, timeout):
    start = asyncio.get_event_loop().time()
    ssl_days_remaining = None
    
    # Check SSL if it's an HTTPS request
    if url.startswith("https://"):
        try:
            hostname = url.split("//")[-1].split("/")[0]
            # Run the sync SSL check in a thread to avoid blocking the event loop
            expiry_date = await asyncio.to_thread(get_ssl_expiry, hostname)
            ssl_days_remaining = (expiry_date - datetime.now(expiry_date.tzinfo)).days
        except Exception:
            ssl_days_remaining = -1 # Indicates an error fetching SSL info

    try:
        async with session.get(url, timeout=timeout) as response:
            latency = (asyncio.get_event_loop().time() - start) * 1000
            
            return {
                "service": name,
                "url": url,
                "status": "ok" if response.status < 400 else "http_error",
                "http_status": response.status,
                "latency_ms": round(latency, 2),
                "ssl_days_remaining": ssl_days_remaining
            }
    except asyncio.TimeoutError:
        return {"service": name, "url": url, "status": "timeout"}
    except aiohttp.ClientConnectionError:
        return {"service": name, "url": url, "status": "connection_error"}
    except Exception as e:
        return {"service": name, "url": url, "status": "unknown_error", "error": str(e)}