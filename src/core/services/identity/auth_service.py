from urllib.parse import quote, unquote, urlparse
from fastapi import Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.common.config.env_config import EnvConfig
from src.core.services.identity.user_command_service import UserCommandService
from src.core.services.identity.login_activity_command_service import LoginActivityCommandService
from src.core.schemas.identity.identity_requests import LoginRequest
from src.common.mail.email_service import EmailService
from src.core.schemas.identity.user_requests import PasswordRecoveryRequest
from src.core.services.identity.user_query_service import UserQueryService
from src.core.services.identity.token_blacklist_service import TokenBlackListService
from src.common.utils.messages.identity_messsages import AuthMsg, UserMsg
from src.core.services.identity.jwt_service import JwtService
from src.common.utils.custom_exceptions import *
from src.core.schemas.identity.user_responses import UserDetail


class AuthService:

    def __init__(self, db: AsyncIOMotorDatabase):
        self.user_query_service = UserQueryService(db)
        self.user_command_service = UserCommandService(db)
        self.activity_service = LoginActivityCommandService(db)
        self.email_service = EmailService()


    async def login(self, request: Request, body: LoginRequest) -> JSONResponse:
        user = await self.user_command_service.authenticate_user(body.email, body.password)
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
        # login activity
        await self.activity_service.update_login(request, user)
        return response


    async def refresh_access_token(self, request: Request) -> RedirectResponse:
        refresh_token = JwtService.get_token_from_cookie(request, EnvConfig.JWT_COOKIE_REFRESH_NAME)
        payload = await JwtService.verify_token(refresh_token, refresh=True)
       
        if not payload:
            return JSONResponse({"detail": AuthMsg.Error.INVALID_REFRESH_TOKEN}, status_code=status.HTTP_401_UNAUTHORIZED)

        user = await self.user_query_service.get_user_by_id(payload["sub"])
        if not user:
            return JSONResponse({"detail": UserMsg.Error.NOT_FOUND}, status_code=status.HTTP_404_NOT_FOUND)

        new_access_token = JwtService.create_access_token(user)
        response = JSONResponse({"accessToken": new_access_token})
        JwtService.set_access_cookie(response, new_access_token)
        return response


    async def get_current_user(self, request: Request) -> UserDetail:
        payload = await JwtService.extract_payload(request)
        user = await self.user_query_service.get_user_by_id(payload["sub"])
        if not user:
            raise NotFoundException(UserMsg.Error.NOT_FOUND)
        return user


    async def logout(self, request: Request) -> JSONResponse:
        current_user = await self.get_current_user(request)
        token = JwtService.get_token_from_cookie(request, EnvConfig.JWT_COOKIE_ACCESS_NAME)
        if token:
            await TokenBlackListService.add_token(token)
        # login activity
        user = await self.user_command_service.get_user_by_email_aux(current_user.email)
        await self.activity_service.update_logout(request, user)
        # send response
        response = JSONResponse(AuthMsg.Success.USER_LOGGED_OUT.format(current_user.email), status_code=status.HTTP_200_OK)
        JwtService.clear_cookies(response)
        return response


    async def get_password_recovery_link(self, request: Request, body: PasswordRecoveryRequest):
        user = await self.user_command_service.get_user_by_email_aux(body.email)
        if not user:
            raise InternalServerErrorException(f"User with email '{body.email}' does not exist.")
        
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
