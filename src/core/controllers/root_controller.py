from pathlib import Path
from fastapi import APIRouter, Request, status
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from src.common.config.template_config import TemplateConfig


class RootController:

    def __init__(self):
        self.download_path = Path("docs/api_collections/Insomnia.yaml")

    async def index(self, request: Request):
        return TemplateConfig.templates.TemplateResponse("index.html", {
            "request": request,
            "title": "API Root - MongoDB API",
        })
    
    async def download_collections(self):
        if self.download_path.exists():
            return FileResponse(
                path=str(self.download_path),
                filename="Insomnia.yaml",
                media_type="application/x-yaml"
            )
        return HTMLResponse("<h3>File not found</h3>", status_code=status.HTTP_404_NOT_FOUND)
    

    async def health_check(self):
        return JSONResponse({
            "status": "ok",
            "service": "python-mongodb-api",
            "message": "It works. App is running"
        })
        

    @classmethod
    def add_routes(cls) -> APIRouter:
        router = APIRouter()
        controller = RootController()
        router.add_api_route("/", controller.index, methods=["GET"])
        router.add_api_route("/download-collections", controller.download_collections, methods=["GET"])
        router.add_api_route("/health", controller.health_check, methods=["GET"])
        return router
    
