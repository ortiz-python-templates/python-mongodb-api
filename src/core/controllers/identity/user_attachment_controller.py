from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import APIRouter, Depends, Form, Request, UploadFile, status
from fastapi.responses import JSONResponse
from src.core.services.identity.user_attachment_query_service import UserAttachmentQueryService
from src.core.services.identity.user_attachment_command_service import UserAttachmentCommandService
from src.core.filters.pagination_filter import PaginationFilter
from src.core.filters.search_filter  import SearchFilter
from src.common.middlewares.authorization_middleware import AuthorizationMiddleware as authz
from src.core.schemas.pagination_response import *
from src.core.schemas.identity.user_requests import *
from src.common.utils.messages.identity_messsages import *
from src.common.utils.custom_exceptions import *


class UserAttachmentController:

    def __init__(self, db: AsyncIOMotorDatabase):
        self.command_service = UserAttachmentCommandService(db)
        self.query_service = UserAttachmentQueryService(db)

    async def create_user_attachment(self, request: Request, 
                file: UploadFile = Form(...), 
                user_id: str = Form(...), 
                description: str = Form(...)):
        body = CreateUserAttachmentRequest(user_id=user_id, description=description)
        resp = await self.command_service.create_user_attachment(request, file, body)
        return JSONResponse(resp.model_dump(), status.HTTP_201_CREATED)

    async def get_all_user_attachments(self, request: Request, search_filter: SearchFilter=Depends(), pagination_filter: PaginationFilter=Depends()):
        return await self.query_service.get_all_user_attachments(request, search_filter, pagination_filter)
    
    async def get_all_user_attachments_by_user(self, request: Request, user_id: str, pagination_filter: PaginationFilter=Depends()):
        return await self.query_service.get_all_attachments_by_user(request, user_id, pagination_filter)

    async def get_user_attachment_by_id(self, request: Request, attachment_id: str):
        return await self.query_service.get_user_attachment_by_id(attachment_id)

    async def display_user_attachment(self, request: Request, attachment_id: str):
        return await self.query_service.display_user_attachment(request, attachment_id)

    
    @classmethod
    def add_routes(cls, db: AsyncIOMotorDatabase) -> APIRouter:
        router = APIRouter()
        controller = UserAttachmentController(db)
        router.add_api_route("/", controller.get_all_user_attachments, methods=["GET"])
        router.add_api_route("/", controller.create_user_attachment, methods=["POST"])
        router.add_api_route("/by-user/{user_id}", controller.get_all_user_attachments_by_user, methods=["GET"])
        router.add_api_route("/{attachment_id}", controller.get_user_attachment_by_id, methods=["GET"])
        router.add_api_route("/{attachment_id}/display", controller.display_user_attachment, methods=["GET"])
        return router