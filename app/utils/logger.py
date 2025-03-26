from loguru import logger
import sys
from pathlib import Path

LOG_PATH = Path("/tmp/scansioni/logs")
LOG_PATH.mkdir(parents=True, exist_ok=True)

logger.remove()
logger.add(sys.stderr, level="INFO")
logger.add(str(LOG_PATH / "scansioni.log"), rotation="1 MB", retention="7 days", level="DEBUG")

def log_event(event_type: str, message: str):
    logger.info(f"[{event_type}] {message}")