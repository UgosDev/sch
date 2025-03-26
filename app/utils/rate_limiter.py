import time
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict

# Limite: 10 richieste ogni 60 secondi per IP
MAX_REQUESTS = 10
TIME_WINDOW = 60  # secondi

request_log = defaultdict(list)

class RateLimiterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()

        # Pulisce le richieste vecchie
        request_log[client_ip] = [
            timestamp for timestamp in request_log[client_ip]
            if current_time - timestamp < TIME_WINDOW
        ]

        # Verifica se il limite è superato
        if len(request_log[client_ip]) >= MAX_REQUESTS:
            raise HTTPException(status_code=429, detail="Troppi tentativi. Riprova tra poco.")

        # Aggiunge la richiesta corrente
        request_log[client_ip].append(current_time)
        response = await call_next(request)
        return response