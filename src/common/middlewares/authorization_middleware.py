from fastapi import Depends, Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.common.utils.custom_exceptions import ForbiddenException
from src.core.services.identity.jwt_service import JwtService


class AuthorizationMiddleware(BaseHTTPMiddleware):

    @staticmethod
    def require_roles(*allowed_roles: str):
        async def dependency(request: Request):
            payload = await JwtService.extract_payload(request)
            user_roles = payload.get("roles", [])
            if not any(role in user_roles for role in allowed_roles):
                raise ForbiddenException("Access denied. Your role does not have permission to access this resource.")
            return payload
        return Depends(dependency)

    @staticmethod
    def require_permissions(*required_permissions: str):
        async def dependency(request: Request):
            payload = await JwtService.extract_payload(request)
            user_permissions = payload.get("permissions", [])
            if not all(p in user_permissions for p in required_permissions):
                raise ForbiddenException("Access denied. You do not have the required permissions to access this resource.")
            return payload
        return Depends(dependency)
