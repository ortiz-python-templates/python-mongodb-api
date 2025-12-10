from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from src.core.services.identity.user_query_service import UserQueryService
from src.core.services.identity.user_command_service import UserCommandService
from src.core.filters.pagination_filter import PaginationFilter
from src.core.filters.search_filter  import SearchFilter
from src.core.models.identity.role import Role
from src.common.middlewares.authorization_middleware import AuthorizationMiddleware as authz
from src.core.schemas.pagination_response import *
from src.core.schemas.identity.user_requests import *
from src.common.utils.messages.identity_messsages import *
from src.common.utils.custom_exceptions import *


class UserController:

    def __init__(self, db: AsyncIOMotorDatabase):
        self.command_service = UserCommandService(db)
        self.query_service = UserQueryService(db)

    async def create_user(self, body: CreateUserRequest):
        resp = await self.command_service.create_user(body)
        return JSONResponse(resp.model_dump(), status.HTTP_201_CREATED)

    async def get_all_users(self, request: Request, pagination_filter: PaginationFilter=Depends()):
        return await self.query_service.get_all_users(request, pagination_filter)
    
    async def get_all_users_by_status(self, request: Request, status: bool, pagination_filter: PaginationFilter=Depends()):
        return await self.query_service.get_all_users_by_status(request, status, pagination_filter)
    
    async def search_users(self, request: Request, search_filter: SearchFilter=Depends(), pagination_filter: PaginationFilter=Depends()):
        return await self.query_service.search_users(request, search_filter, pagination_filter)

    async def get_user_by_unique_id(self, unique_id: str):
        return await self.query_service.get_user_by_unique_id(unique_id)

    async def get_user_by_email(self, email: str):
        return await self.query_service.get_user_by_email(email)

    async def update_user(self, unique_id: str, body: UpdateUserRequest):
        resp = await self.command_service.update_user(unique_id, body)
        return JSONResponse(resp.model_dump(), status.HTTP_200_OK)

    async def activate_user(self, unique_id: str, body: ActivateUserRequest):
        resp = await self.command_service.activate_user(unique_id, body)
        return JSONResponse(resp.model_dump(), status.HTTP_200_OK)
    
    async def deactivate_user(self, unique_id: str, body: DeactivateUserRequest):
        resp = await self.command_service.deactivate_user(unique_id, body)
        return JSONResponse(resp.model_dump(), status.HTTP_200_OK)
    
    @classmethod
    def add_routes(cls, db: AsyncIOMotorDatabase) -> APIRouter:
        router = APIRouter()
        controller = UserController(db)
        router.add_api_route("/", controller.get_all_users, methods=["GET"])
        router.add_api_route("/search", controller.search_users, methods=["GET"])
        router.add_api_route("/", controller.create_user, methods=["POST"])
        router.add_api_route("/{unique_id}", controller.get_user_by_unique_id, methods=["GET"])
        router.add_api_route("/{unique_id}", controller.update_user, methods=["PUT"])
        router.add_api_route("/by-status/{status}", controller.get_all_users_by_status, methods=["GET"])
        router.add_api_route("/by-email/{email}", controller.get_user_by_email, methods=["GET"])
        router.add_api_route("/{unique_id}/activate", controller.activate_user, methods=["PUT"])
        router.add_api_route("/{unique_id}/deactivate", controller.deactivate_user, methods=["PUT"])
        return router