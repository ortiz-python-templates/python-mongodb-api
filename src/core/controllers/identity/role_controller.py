from fastapi import APIRouter
from src.common.middlewares.authorization_middleware import AuthorizationMiddleware as authz
from src.core.models.identity.role import Role
from src.core.services.identity.role_service import RoleService
from src.common.utils.custom_exceptions import *


class RoleController:

    def __init__(self):
        self.service = RoleService()
       
    async def get_all_roles(self):
        return self.service.get_all_roles()
          
    async def get_role_by_code(self, code: str):
        return self.service.get_role_by_code(code)
          
    @classmethod
    def add_routes(cls) -> APIRouter:
        router = APIRouter()
        controller = RoleController()
        router.add_api_route("/", controller.get_all_roles, methods=["GET"])
        router.add_api_route("/{code}", controller.get_role_by_code, methods=["GET"])
        return router