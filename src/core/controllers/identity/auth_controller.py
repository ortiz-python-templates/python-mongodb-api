from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import APIRouter, Request, status
from src.common.utils.messages.identity_messsages import AuthMsg
from src.core.services.identity.user_command_service import UserCommandService
from src.core.schemas.identity.identity_requests import *
from src.core.schemas.identity.identity_responses import *
from src.core.schemas.identity.user_requests import *
from src.core.services.identity.auth_service import AuthService
from src.common.utils.custom_exceptions import *


class AuthController:

    def __init__(self, db: AsyncIOMotorDatabase):
        self.service = AuthService(db)
        self.user_service = UserCommandService(db)

    async def login(self, body: LoginRequest): 
        return await self.service.login(body)
    
    async def logout(self, request: Request): 
        return await self.service.logout(request)
        
    async def refresh_access_token(self, request: Request, next: str = "") -> JSONResponse:
        return await self.service.refresh_access_token(request, next)
      
    async def get_current_user(self, request: Request):
        return await self.service.get_current_user(request)
     
    async def register_user(self, body: RegisterUserRequest):
        await self.user_service.register_user(body)
        return JSONResponse(AuthMsg.Success.USER_REGISTERED.format(body.email), status.HTTP_201_CREATED)
    
    async def get_password_recovery_link(self, request: Request, body: PasswordRecoveryRequest):
        await self.service.get_recovery_link(request, body)
        return JSONResponse(AuthMsg.Success.EMAIL_SENT, status.HTTP_200_OK)
    
    async def reset_password(self, token: str, body: ResetPasswordRequest):
        await self.service.reset_password(token, body)
        return JSONResponse(AuthMsg.Success.PASSWORD_RESET, status.HTTP_200_OK)


    @classmethod
    def add_routes(cls, db: AsyncIOMotorDatabase) -> APIRouter:
        router = APIRouter()
        controller = AuthController(db)
        router.add_api_route("/login", controller.login, methods=["POST"])
        router.add_api_route("/logout", controller.logout, methods=["GET"])
        router.add_api_route("/refresh-token", controller.refresh_access_token, methods=["GET"])
        router.add_api_route("/current-user", controller.get_current_user, methods=["GET"])
        router.add_api_route("/register", controller.register_user, methods=["POST"])
        router.add_api_route("/get-recover-link", controller.get_password_recovery_link, methods=["POST"])
        router.add_api_route("/reset-password/{token}", controller.reset_password, methods=["POST"])
        return router
