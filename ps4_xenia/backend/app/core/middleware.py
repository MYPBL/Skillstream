"""
Middleware configuration for the application.
Includes Rate Limiting setup using slowapi.
"""
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging

# Setup Logger
logger = logging.getLogger("api_aspects")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

# Setup Limiter
limiter = Limiter(key_func=get_remote_address)

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response

class AuditLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Log all write operations and auth attempts
        if request.method in ["POST", "PUT", "DELETE"] or "auth" in request.url.path:
            logger.info(
                f"AUDIT: {request.method} {request.url.path} "
                f"Status: {response.status_code} "
                f"Time: {process_time:.4f}s "
                f"IP: {request.client.host}"
            )
        return response

def setup_middleware(app: FastAPI):
    # Add Rate Limit Exception Handler
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    
    # Add Security Headers
    app.add_middleware(SecurityHeadersMiddleware)
    
    # Add Audit Logging
    app.add_middleware(AuditLogMiddleware)
