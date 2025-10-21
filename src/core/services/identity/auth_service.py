from urllib.parse import quote, unquote, urlparse
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse, RedirectResponse
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.core.schemas.identity.identity_requests import LoginRequest
from src.common.mail.email_service import EmailService
from src.common.utils.encryption_util import EncryptionUtil
from src.common.utils.password_util import PasswordUtil
from src.core.repositories.identity.user_command_repository import UserCommandRepository
from src.core.repositories.identity.user_query_repository import UserQueryRepository
from src.core.schemas.identity.user_requests import PasswordRecoveryRequest, ResetPasswordRequest
from src.core.services.identity.user_query_service import UserQueryService
from src.core.services.identity.token_blacklist_service import TokenBlackListService
from src.common.utils.messages.identity_messsages import AuthMsg, UserMsg
from src.core.services.identity.jwt_service import JwtService
from src.common.utils.custom_exceptions import *
from src.core.schemas.identity.user_responses import UserDetail


class AuthService:

    def __init__(self, db: AsyncIOMotorDatabase):
        self.user_service = UserQueryService(db)
        self.command_repository = UserCommandRepository(db)
        self.query_repository = UserQueryRepository(db)
        self.email_service = EmailService()


    async def login(self, body: LoginRequest) -> JSONResponse:
        user = await self.user_service.authenticate_user(body.email, body.password)
        if not user:
            raise UnauthorizedException(AuthMsg.Error.INVALID_CREDENTIALS)

        access_token = JwtService.create_access_token(user)
        refresh_token = JwtService.create_refresh_token(user)

        response = JSONResponse(content={
            "accessToken": access_token,
            "refreshToken": refresh_token
        })
        JwtService.set_access_cookie(response, access_token)
        JwtService.set_refresh_cookie(response, refresh_token)
        return response


    async def refresh_access_token(self, request: Request, next: str) -> RedirectResponse:
        refresh_token = JwtService.get_token_from_cookie(request, "refresh_token")
        payload = await JwtService.verify_token(refresh_token, refresh=True)
       
        if not payload:
            return JSONResponse({"detail": AuthMsg.Error.INVALID_REFRESH_TOKEN}, status_code=status.HTTP_401_UNAUTHORIZED)

        user = await self.user_service.get_user_by_unique_id(payload["sub"])
        if not user:
            return JSONResponse({"detail": UserMsg.Error.NOT_FOUND}, status_code=status.HTTP_404_NOT_FOUND)

        new_access_token = JwtService.create_access_token(user)
        response = JSONResponse({"accessToken": new_access_token})
        JwtService.set_access_cookie(response, new_access_token)
        return response


    async def get_current_user(self, request: Request) -> UserDetail:
        payload = await JwtService.extract_payload(request)
        user = await self.user_service.get_user_by_unique_id(payload["sub"])
        if not user:
            raise NotFoundException(UserMsg.Error.NOT_FOUND)
        return user


    async def logout(self, request: Request) -> JSONResponse:
        user = await self.get_current_user(request)
        token = JwtService.get_token_from_cookie(request, "access_token")
        if token:
            await TokenBlackListService.add_token(token)
        response = JSONResponse(AuthMsg.Success.USER_LOGGED_OUT.format(user.email), status_code=status.HTTP_200_OK)
        JwtService.clear_cookies(response)
        return response


    async def get_recovery_link(self, request: Request, body: PasswordRecoveryRequest):
        user = await self.command_repository.get_by_email_aux(body.email)
        if not user:
            raise InternalServerErrorException(f"Usuário com Email '{body.email}' não existe")
        
        base_url = f"{request.url.scheme}://{request.url.netloc}"
        reset_link = f"{base_url}/reset-password?token={user.recovery_token}"

        await self.email_service.send_email(
            subject="Password Recovery",
            email_to=body.email,
            template_name="email/reset-password.html",
            context={
                "reset_link": reset_link,
                "email": user.email
            }
        )


    async def reset_password(self, token: str, body: ResetPasswordRequest):
        user = await self.command_repository.get_by_recovery_token_aux(token)
        if not user:
            raise BadRequestException("Token de recuperação inválido ou expirado.")
        if not user.is_active:
            raise BadRequestException("Sua conta está inativa no momento. Entre em contato com o suporte para reativá-la.")
        user.password = PasswordUtil.hash(body.new_password)
        user.recovery_token = EncryptionUtil.generate_random_token(32)
        self.command_repository.update(user.id, user)