from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from pathlib import Path
import json

API_KEYS_PATH = Path(__file__).parent / "api_keys.json"

def load_api_keys():
    with API_KEYS_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)

class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        api_key = request.headers.get("X-API-Key")
        valid_keys = load_api_keys()

        if not api_key or api_key not in valid_keys:
            raise HTTPException(status_code=401, detail="API key mancante o non valida")
        response = await call_next(request)
        return response