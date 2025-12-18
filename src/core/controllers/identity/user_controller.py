from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import APIRouter, Depends, Request, UploadFile, status
from fastapi.responses import JSONResponse
from src.core.services.identity.user_query_service import UserQueryService
from src.core.services.identity.user_command_service import UserCommandService
from src.core.shared.filters.pagination_filter import PaginationFilter
from src.core.shared.filters.search_filter  import SearchFilter
from src.core.models.identity.role import Role
from src.common.middlewares.authorization_middleware import AuthorizationMiddleware as authz
from src.core.shared.schemas.pagination_response import *
from src.core.schemas.identity.user_requests import *
from src.common.utils.messages.identity_messsages import *
from src.common.utils.custom_exceptions import *


class UserController:

    def __init__(self, db: AsyncIOMotorDatabase):
        self.command_service = UserCommandService(db)
        self.query_service = UserQueryService(db)

    async def create_user(self, request: Request, body: CreateUserRequest):
        resp = await self.command_service.create_user(request, body)
        return JSONResponse(resp.model_dump(), status.HTTP_201_CREATED)

    async def get_all_users(self, request: Request, search_filter: SearchFilter=Depends(), pagination_filter: PaginationFilter=Depends()):
        return await self.query_service.get_all_users(request, search_filter, pagination_filter)
    
    async def get_active_users(self, request: Request, pagination_filter: PaginationFilter=Depends()):
        return await self.query_service.get_active_users(request, pagination_filter)
    
    async def get_inactive_users(self, request: Request, pagination_filter: PaginationFilter=Depends()):
        return await self.query_service.get_inactive_users(request, pagination_filter)

    async def get_user_by_id(self, request: Request, id: str):
        return await self.query_service.get_user_by_id(id)

    async def get_user_by_email(self, request: Request, email: str):
        return await self.query_service.get_user_by_email(email)

    async def update_user(self, request: Request, id: str, body: UpdateUserRequest):
        resp = await self.command_service.update_user(request, id, body)
        return JSONResponse(resp.model_dump(), status.HTTP_200_OK)
    
    async def update_user_avatar(self, request: Request, id: str, file: UploadFile):
        resp = await self.command_service.update_user_avatar(request, id, file)
        return JSONResponse(resp.model_dump(), status.HTTP_200_OK)

    async def activate_user(self, request: Request, id: str, body: ActivateUserRequest):
        resp = await self.command_service.activate_user(request, id, body)
        return JSONResponse(resp.model_dump(), status.HTTP_200_OK)
    
    async def deactivate_user(self, request: Request, id: str, body: DeactivateUserRequest):
        resp = await self.command_service.deactivate_user(request, id, body)
        return JSONResponse(resp.model_dump(), status.HTTP_200_OK)
    
    @classmethod
    def add_routes(cls, db: AsyncIOMotorDatabase) -> APIRouter:
        router = APIRouter()
        controller = UserController(db)
        router.add_api_route("/", controller.get_all_users, methods=["GET"])
        router.add_api_route("/actives", controller.get_active_users, methods=["GET"])
        router.add_api_route("/inactives", controller.get_inactive_users, methods=["GET"])
        router.add_api_route("/", controller.create_user, methods=["POST"])
        router.add_api_route("/{id}", controller.get_user_by_id, methods=["GET"])
        router.add_api_route("/{id}", controller.update_user, methods=["PUT"])
        router.add_api_route("/by-email/{email}", controller.get_user_by_email, methods=["GET"])
        router.add_api_route("/{id}/avatars", controller.update_user_avatar, methods=["PATCH"])
        router.add_api_route("/{id}/activate", controller.activate_user, methods=["PATCH"])
        router.add_api_route("/{id}/deactivate", controller.deactivate_user, methods=["PATCH"])
        return router