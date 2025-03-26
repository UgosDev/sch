from fastapi import FastAPI
from app.api.v1 import scan, download
from app.utils.rate_limiter import RateLimiterMiddleware
from app.utils.auth import APIKeyMiddleware

app = FastAPI()
app.add_middleware(APIKeyMiddleware)
app.add_middleware(RateLimiterMiddleware)

app.include_router(scan.router, prefix="/api/v1")
app.include_router(download.router, prefix="/api/v1")