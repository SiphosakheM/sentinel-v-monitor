Sentinel-V: Asynchronous Health and Latency Monitor

Architecture Overview

Sentinel-V is a high-concurrency monitoring tool that provides real-time visibility into distributed service clusters. It uses an asynchronous event loop to reduce resource use while increasing throughput.

Features

- Async Probing: Runs health checks in parallel using aiohttp.
- Deep SSL Inspection: Monitors TLS certificate expiration proactively.
- Structured Observability: Offers JSON-formatted logs suitable for ELK and Grafana integration.
- Config-Driven: Scales easily via endpoints.yaml.

Tech Stack

- Runtime: Python 3.10 or higher
- Core Libraries: asyncio, aiohttp, cryptography
- Configuration: PyYAML
- Logging: structlog

Prerequisites

- Python 3.10 or higher installed.
- Virtual environment (venv) is recommended.

Installation and Setup

- Clone the repository: git clone https://github.com/your-username/sentinel-v-monitor.git
- Set up the environment: python -m venv venv; source venv/bin/activate # Or venv\Scripts\activate on Windows
- Install dependencies: pip install -r requirements.txt

Usage

- Define your targets in config/endpoints.yaml.
- Run the monitor: python main.py
