import json
from pathlib import Path
from datetime import datetime

COUNTER_FILE = Path("/tmp/scansioni/api_counters.json")

def load_counters():
    if COUNTER_FILE.exists():
        with COUNTER_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_counters(data):
    with COUNTER_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def increment_counter(api_key: str):
    counters = load_counters()
    today = datetime.utcnow().strftime("%Y-%m-%d")

    if api_key not in counters:
        counters[api_key] = {}
    if today not in counters[api_key]:
        counters[api_key][today] = 0

    counters[api_key][today] += 1
    save_counters(counters)
    return counters[api_key][today]