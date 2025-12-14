from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import APIRouter, Depends, Request
from src.core.filters.search_filter import SearchFilter
from src.core.filters.pagination_filter import PaginationFilter
from src.core.schemas.configurations.feature_flag_requests import ManageFeatureFlagRequest
from src.core.services.configurations.feature_flag_service import FeatureFlagService
from src.common.middlewares.authorization_middleware import AuthorizationMiddleware as authz
from src.core.schemas.pagination_response import *
from src.common.utils.messages.identity_messsages import *
from src.common.utils.custom_exceptions import *


class FeatureFlagController:

    def __init__(self, db: AsyncIOMotorDatabase):
        self.service = FeatureFlagService(db)

    async def manage_feature_flags(self, request: Request, body: ManageFeatureFlagRequest):
        return await self.service.manage_feature_flag(request, body)
    
    async def get_all_feature_flags(self, request: Request, search_filter: SearchFilter=Depends(), pagination_filter: PaginationFilter=Depends()):
        return await self.service.get_all_feature_flags(request, search_filter, pagination_filter)
    
    async def get_feature_flag_by_id(self, request: Request, id: str):
        return await self.service.get_feature_flag_by_id(request, id)

    async def get_feature_flag_by_name(self, request: Request, name: str):
        return await self.service.get_feature_flag_by_name(request, name)
    
    @classmethod
    def add_routes(cls, db: AsyncIOMotorDatabase) -> APIRouter:
        router = APIRouter()
        controller = FeatureFlagController(db)
        router.add_api_route("/", controller.get_all_feature_flags, methods=["GET"])
        router.add_api_route("/", controller.manage_feature_flags, methods=["PUT"])
        router.add_api_route("/by-name/{name}", controller.get_feature_flag_by_name, methods=["GET"])
        router.add_api_route("/{id}", controller.get_feature_flag_by_id, methods=["GET"])
        return router