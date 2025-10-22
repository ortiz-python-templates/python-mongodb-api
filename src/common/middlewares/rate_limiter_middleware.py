from fastapi.responses import JSONResponse
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.common.config.env_config import EnvConfig
from src.common.utils.custom_exceptions import ForbiddenException
from src.core.services.identity.jwt_service import JwtService
from src.common.config.redis_client import RedisClient


class RateLimiterMiddleware(BaseHTTPMiddleware):

    _excluded_paths = {
        "/",
        "/health",
        "/metrics",
        "/favicon.ico",
        "/api/auth/get-recovery-token",
        "/api/auth/login",
        "/api/auth/register",
        "/docs",
        "/redoc",
        "/openapi.json"
    }
    
    _public_prefixes = (
        "/public/static/",
        "/static/",
    )

    def __init__(self, app):
        super().__init__(app)
        self.max_requests = EnvConfig.RATE_LIMIT_MAX_REQUESTS
        self.window_seconds = EnvConfig.RATE_LIMIT_WINDOW_SECONDS
        # Endpoints that don’t need rate limiting (public endpoints)
        
    async def dispatch(self, request: Request, call_next):
        path = request.url.path 
        # Skip rate limiting for public endpoints
        if path in self._excluded_paths or any(path.startswith(prefix) for prefix in self._public_prefixes):
            response = await call_next(request)
            return response 
        
        try:
            payload = await JwtService.extract_payload(request)
            user_unique_id = payload["sub"]
            if not user_unique_id:
                raise ForbiddenException("Invalid token: user ID not found.")

            redis_key = f"rate_limit:{user_unique_id}"
            count = await RedisClient.incr(redis_key)
            
            if count == 1:
                await RedisClient.expire(redis_key, self.window_seconds)

            if count > self.max_requests:
                return JSONResponse(
                    status_code=429,
                    content={
                        "detail": (
                            f"You have exceeded the limit of {self.max_requests} requests. "
                            f"Try again after {self.window_seconds} seconds."
                        )
                    }
                )

        except ForbiddenException as e:
            return JSONResponse(
                status_code=403,
                content={"detail": e.detail}
            )
        except Exception as e:
            print(f"[RateLimiterMiddleware] Unexpected error: {e}")

        response = await call_next(request)
        return response
