from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import APIRouter, Depends, Request
from src.core.schemas.configurations.basic_configuration_requests import UpdateBasicConfigurationRequest
from src.core.services.configurations.basic_configuration_service import BasicConfigurationService
from src.common.middlewares.authorization_middleware import AuthorizationMiddleware as authz
from src.core.shared.schemas.pagination_response import *
from src.common.utils.messages.identity_messsages import *
from src.common.utils.custom_exceptions import *


class BasicConfigurationController:

    def __init__(self, db: AsyncIOMotorDatabase):
        self.service = BasicConfigurationService(db)

    async def update_basic_configurations(self, request: Request, body: UpdateBasicConfigurationRequest):
        return await self.service.update_basic_configuration(request, body)
    
    async def get_basic_configurations(self, request: Request):
        return await self.service.get_basic_configurations(request)
    
    @classmethod
    def add_routes(cls, db: AsyncIOMotorDatabase) -> APIRouter:
        router = APIRouter()
        controller = BasicConfigurationController(db)
        router.add_api_route("/", controller.update_basic_configurations, methods=["PUT"])
        router.add_api_route("/", controller.get_basic_configurations, methods=["GET"])
        return router