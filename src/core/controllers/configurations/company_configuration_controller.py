from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import APIRouter, Depends, Request
from src.core.schemas.configurations.company_configuration_requests import UpdateCompanyConfigurationRequest
from src.core.services.configurations.company_configuration_service import CompanyConfigurationService
from src.common.middlewares.authorization_middleware import AuthorizationMiddleware as authz
from src.core.shared.schemas.pagination_response import *
from src.common.utils.messages.identity_messsages import *
from src.common.utils.custom_exceptions import *


class CompanyConfigurationController:

    def __init__(self, db: AsyncIOMotorDatabase):
        self.service = CompanyConfigurationService(db)

    async def update_company_configurations(self, request: Request, body: UpdateCompanyConfigurationRequest):
        return await self.service.update_company_configuration(request, body)
    
    async def get_company_configurations(self, request: Request):
        return await self.service.get_company_configurations(request)
    
    @classmethod
    def add_routes(cls, db: AsyncIOMotorDatabase) -> APIRouter:
        router = APIRouter()
        controller = CompanyConfigurationController(db)
        router.add_api_route("/", controller.update_company_configurations, methods=["PUT"])
        router.add_api_route("/", controller.get_company_configurations, methods=["GET"])
        return router