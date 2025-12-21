from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import APIRouter, Depends, Form, Request, Response, UploadFile, status
from src.core.services.files.file_query_service import FileQueryService
from src.core.models.files.enums import FileVisibility
from src.core.schemas.files.file_requests import UploadFileRequest
from src.core.services.files.file_command_service import FileCommandService
from src.core.shared.filters.pagination_filter import PaginationFilter
from src.core.shared.filters.search_filter import SearchFilter


class FileController:

    def __init__(self, db: AsyncIOMotorDatabase):
       self.command_service = FileCommandService(db)
       self.query_service = FileQueryService(db)

    async def upload_file(self, request: Request,   
            file: UploadFile = Form(...), 
            category: str = Form(...),
            owner_entity: str = Form(...),
            owner_id: str = Form(...),
            display_name: str = Form(...),
            description: str = Form(...),
            visibility: FileVisibility = Form(...),
            ):
        
        body = UploadFileRequest(
            category=category,
            owner_entity=owner_entity,
            owner_id=owner_id,
            display_name=display_name,
            description=description,
            visibility=visibility
        )
        resp = await self.command_service.upload_file(request, file, body)
        return JSONResponse(resp.model_dump(), status.HTTP_201_CREATED)
    
    async def downlad_file(self, request: Request, file_id: str):
        return await self.command_service.download_file(request, file_id)

    async def display_file(self, request: Request, file_id: str):
        return await self.command_service.display_file(request, file_id)
    
    async def get_all_files(self, request: Request, search_filter: SearchFilter=Depends(), pagination_filter: PaginationFilter=Depends()):
        return await self.query_service.get_all_files(request, search_filter, pagination_filter)
    
    async def get_all_files_by_category(self, request: Request, category: str, search_filter: SearchFilter=Depends(), pagination_filter: PaginationFilter=Depends()):
        return await self.query_service.get_all_files_by_category(request, category, search_filter, pagination_filter)

    async def get_all_files_by_user(self, request: Request, user_id: str, search_filter: SearchFilter=Depends(), pagination_filter: PaginationFilter=Depends()):
        return await self.query_service.get_all_files_by_user(request, user_id, search_filter, pagination_filter)
    
    async def get_all_files_by_owner_entity(self, request: Request, owner_entity: str, search_filter: SearchFilter=Depends(), pagination_filter: PaginationFilter=Depends()):
        return await self.query_service.get_all_files_by_owner_entity(request, owner_entity, search_filter, pagination_filter)

    async def get_all_files_by_owner_id(self, request: Request, owner_id: str, search_filter: SearchFilter=Depends(), pagination_filter: PaginationFilter=Depends()):
        return await self.query_service.get_all_files_by_owner_id(request, owner_id, search_filter, pagination_filter)

    async def get_file_by_id(self, request: Request, file_id: str):
        return await self.query_service.get_file_by_id(request, file_id)
    
    async def get_file_by_name(self, request: Request, name: str):
       return await self.query_service.get_file_by_name(request, name)

    async def delete_file(self, request: Request, file_id: str):
        await self.command_service.delete_file(request, file_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    
    @classmethod
    def add_routes(cls, db: AsyncIOMotorDatabase) -> APIRouter:
        router = APIRouter()
        controller = FileController(db)
    
        router.add_api_route("/upload", controller.upload_file, methods=["POST"])
        router.add_api_route("/by-user/{user_id}", controller.get_all_files_by_user, methods=["GET"])
        router.add_api_route("/by-category/{category}", controller.get_all_files_by_category, methods=["GET"])
        router.add_api_route("/by-owner-entity/{owner_entity}", controller.get_all_files_by_owner_entity, methods=["GET"])
        router.add_api_route("/by-owner-id/{owner_id}", controller.get_all_files_by_owner_id, methods=["GET"])
        router.add_api_route("/by-name/{name}", controller.get_file_by_name, methods=["GET"])
        router.add_api_route("/", controller.get_all_files, methods=["GET"])
        router.add_api_route("/{file_id}", controller.get_file_by_id, methods=["GET"])
        router.add_api_route("/{file_id}", controller.delete_file, methods=["DELETE"])
        router.add_api_route("/{file_id}/download", controller.downlad_file, methods=["GET"])
        router.add_api_route("/{file_id}/display", controller.display_file, methods=["GET"])
        return router