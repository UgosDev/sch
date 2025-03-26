from datetime import datetime
from pathlib import Path

LOG_PATH = Path("/tmp/scansioni/api_usage.log")

def log_api_usage(api_key: str, filename: str):
    timestamp = datetime.utcnow().isoformat()
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(f"{timestamp} - {api_key} - {filename}\n")