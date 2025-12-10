from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from src.core.services.identity.user_query_service import UserQueryService
from src.common.utils.custom_exceptions import UnauthorizedException
from src.core.services.identity.jwt_service import JwtService


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """
    Middleware responsible for JWT authentication.
    Skips public routes (docs, static files, etc.).
    """

    _public_routes = {
        "/",
        "/health",
        "/health/db",
        "/health/redis",
        "/metrics",
        "/download-collections",
        "/favicon.ico",
        "/docs",
        "/openapi.json",
        "/redoc",
        "/api/auth/login",
        "/api/auth/refresh-access-token",
        "/api/auth/register",
        "/api/auth/get-recovery-token",
    }

    _static_routes = (
        "/public/static/",
        "/static/",
    )

    def __init__(self, app, db: AsyncIOMotorDatabase):
        super().__init__(app)
        self.user_service = UserQueryService(db)

    async def dispatch(self, request: Request, call_next):
        try:
            #path = request.url.path
            path = request.url.path.rstrip("/")

            # Allow CORS preflight requests
            if request.method == "OPTIONS":
                return await call_next(request)

            # Allow public routes or static resources
            if (path in self._public_routes or 
                any(path.startswith(prefix) for prefix in self._static_routes)):
                return await call_next(request)

            # Extract and validate JWT payload
            payload = await JwtService.extract_payload(request)
            user = await self.user_service.get_user_by_unique_id(payload.get("sub"))

            if not user:
                raise UnauthorizedException("User not found.")

            # Inject authenticated user into request context
            request.state.user = user

            # Continue request processing
            return await call_next(request)

        except UnauthorizedException as e:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": e.detail},
            )
