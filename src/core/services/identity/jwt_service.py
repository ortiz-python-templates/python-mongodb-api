from datetime import datetime, timedelta
from typing import Dict
from fastapi import Request, Response
from jose import JWTError, jwt
from src.core.schemas.identity.user_responses import UserDetail
from src.core.models.identity.user_model import UserModel
from src.core.services.identity.token_blacklist_service import TokenBlackListService
from src.common.utils.custom_exceptions import UnauthorizedException
from src.common.config.env_config import EnvConfig


class JwtService:

    @staticmethod
    def create_access_token(user: UserDetail) -> str:
        payload = {
            "sub": user.id,
            "email": user.email,
            "roles": [user.role],
            "exp": datetime.now() + timedelta(minutes=EnvConfig.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        return jwt.encode(payload, EnvConfig.JWT_SECRET_KEY, algorithm=EnvConfig.JWT_ALGORITHM)


    @staticmethod
    def create_refresh_token(user: UserDetail) -> str:
        payload = {
            "sub": user.id,
            "email": user.email,
            "exp": datetime.now() + timedelta(days=EnvConfig.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
        }
        return jwt.encode(payload, EnvConfig.JWT_REFRESH_SECRET_KEY, algorithm=EnvConfig.JWT_ALGORITHM)


    @staticmethod
    async def verify_token(token: str, refresh: bool = False):
        if not token:
            raise UnauthorizedException("Missing token. Please log in again.")
        secret = EnvConfig.JWT_REFRESH_SECRET_KEY if refresh else EnvConfig.JWT_SECRET_KEY

        try:
            payload = jwt.decode(token, secret, algorithms=[EnvConfig.JWT_ALGORITHM])
        except JWTError:
            raise UnauthorizedException("Invalid or expired token.")

        if not refresh and await TokenBlackListService.is_blacklisted(token):
            raise UnauthorizedException("Access token is no longer valid. Please log in again.")

        return payload


    @staticmethod
    async def extract_payload(request: Request) -> Dict:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
        else:
            token = request.cookies.get("access_token")

        if not token:
            raise UnauthorizedException("Access token missing in header or cookie.")

        payload = await JwtService.verify_token(token)
        if not payload:
            raise UnauthorizedException("Invalid or expired token.")

        return payload


    @staticmethod
    def set_access_cookie(response: Response, token: str):
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=EnvConfig.is_production(),
            samesite="Lax",
            max_age=EnvConfig.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            path="/",
            domain=EnvConfig.JWT_COOKIE_DOMAIN
        )


    @staticmethod
    def set_refresh_cookie(response: Response, token: str):
        response.set_cookie(
            key="refresh_token",
            value=token,
            httponly=True,
            secure=EnvConfig.is_production(),
            samesite="Lax",
            max_age=EnvConfig.JWT_REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
            path="/",
            domain=EnvConfig.JWT_COOKIE_DOMAIN
        )


    @staticmethod
    def get_token_from_cookie(request: Request, token_name: str):
        return request.cookies.get(token_name)


    @staticmethod
    def clear_cookies(response: Response):
        response.delete_cookie(key="access_token", path="/")
        response.delete_cookie(key="refresh_token", path="/")
