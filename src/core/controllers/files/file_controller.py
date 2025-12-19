from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import APIRouter, Depends, Request, UploadFile, status

from core.shared.filters.pagination_filter import PaginationFilter
from core.shared.filters.search_filter import SearchFilter

class FilesController:

    def __init__(self, db: AsyncIOMotorDatabase):
       pass

    async def upload_file(self, request: Request, file: UploadFile):
        resp = {}
        return JSONResponse(resp.model_dump(), status.HTTP_201_CREATED)
    
    async def downlad_file(self, request: Request, file_id: str):
        pass

    async def display_file(self, request: Request, file_id: str):
        pass

    async def get_all_files_by_user(self, request: Request, user_id: str, search_filter: SearchFilter=Depends(), pagination_filter: PaginationFilter=Depends()):
        pass
    
    async def get_all_files_by_entity(self, request: Request, entity_id: str, search_filter: SearchFilter=Depends(), pagination_filter: PaginationFilter=Depends()):
        pass

    async def get_file_by_id(self, request: Request, file_id: str):
        pass
    
    async def get_file_by_name(self, request: Request, name: str):
        pass

    async def delete_file(self, request: Request, file_id: str):
        return JSONResponse(status.HTTP_204_NO_CONTENT)

    


    @classmethod
    def add_routes(cls, db: AsyncIOMotorDatabase) -> APIRouter:
        router = APIRouter()
        controller = FilesController(db)
    
        router.add_api_route("/upload", controller.upload_file, methods=["POST"])
        router.add_api_route("/by-user/{user_id}", controller.get_all_files_by_user, methods=["GET"])
        router.add_api_route("/by-entity/{entity_id}", controller.get_all_files_by_entity, methods=["GET"])
        router.add_api_route("/by-name/{name}", controller.get_file_by_name, methods=["GET"])
        router.add_api_route("/{file_id}/download", controller.downlad_file, methods=["GET"])
        router.add_api_route("/{file_id}/display", controller.display_file, methods=["GET"])
        router.add_api_route("/{file_id}", controller.get_file_by_id, methods=["GET"])
        router.add_api_route("/{file_id}", controller.delete_file, methods=["DELETE"])
        return router