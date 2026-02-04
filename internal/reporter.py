import json
import logging

logger = logging.getLogger("sentinel")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(message)s"))
logger.addHandler(handler)

def report(event):
    logger.info(json.dumps(event))