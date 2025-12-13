from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import APIRouter, Depends, Request
from src.core.services.identity.login_activity_query_service import LoginActivityQueryService
from src.core.filters.pagination_filter import PaginationFilter
from src.core.filters.search_filter  import SearchFilter
from src.common.middlewares.authorization_middleware import AuthorizationMiddleware as authz
from src.core.schemas.pagination_response import *
from src.common.utils.messages.identity_messsages import *
from src.common.utils.custom_exceptions import *


class LoginActivityController:

    def __init__(self, db: AsyncIOMotorDatabase):
        self.query_service = LoginActivityQueryService(db)

    async def get_all_login_activities(self, request: Request, pagination_filter: PaginationFilter=Depends(), search_filter: SearchFilter=Depends()):
        return await self.query_service.get_all_login_activities(request, pagination_filter, search_filter)
    
    async def get_login_activity_by_id(self, request: Request, id: str):
        return await self.query_service.get_login_activity_by_id(request, id)

    async def get_login_activity_by_user_id(self, request: Request, user_id: str):
        return await self.query_service.get_login_activity_by_user_id(request, user_id)

    
    @classmethod
    def add_routes(cls, db: AsyncIOMotorDatabase) -> APIRouter:
        router = APIRouter()
        controller = LoginActivityController(db)
        router.add_api_route("/", controller.get_all_login_activities, methods=["GET"])
        router.add_api_route("/by-user/{user_id}", controller.get_login_activity_by_user_id, methods=["GET"])
        router.add_api_route("/{id}", controller.get_login_activity_by_id, methods=["GET"])
        return router