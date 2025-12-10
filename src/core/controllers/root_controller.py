from datetime import datetime
from pathlib import Path
import platform
import socket
from fastapi import APIRouter, Request, status
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from src.common.config.env_config import EnvConfig
from src.common.config.template_config import TemplateConfig
from src.common.config.db_config import DbConfig
from src.common.config.redis_client import RedisClient


# Global start time
app_start_time = datetime.now()

class RootController:

    def __init__(self):
        self.download_path = Path("docs/api_collections/Insomnia.yaml")
        self.db = DbConfig.get_database()


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
        now = datetime.now()
        uptime_seconds = (now - app_start_time).total_seconds()
        return JSONResponse({
            "status": "ok",
            "service": EnvConfig.APP_NAME,
            "message": "It works. App is running",
            "uptime_seconds": uptime_seconds,
            "hostname": socket.gethostname(),
            "python_version": platform.python_version(),
            "version": EnvConfig.APP_VERSION  
        })


    async def health_check_db(self):
        try:
            await self.db.client.admin.command("ping")
            mongo_status = "ok"
        except Exception as e:
            mongo_status = f"error: {e}"
        status_code = status.HTTP_200_OK if mongo_status == "ok" else status.HTTP_503_SERVICE_UNAVAILABLE
        return JSONResponse({
            "status": mongo_status,
            "service": EnvConfig.APP_NAME,
            "message": "MongoDB health check"
        }, status_code=status_code)


    async def health_check_redis(self):
        try:
            await RedisClient.init()
            pong = await RedisClient._redis.ping() 
            return JSONResponse({
                "status": "ok",
                "service": "python-template-mongodb-api",
                "message": "Redis is reachable"
            })
        except Exception as e:
            return JSONResponse({
                "status": f"error: {e}",
                "service": "python-template-mongodb-api",
                "message": "Redis health check"
            }, status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


    @classmethod
    def add_routes(cls) -> APIRouter:
        router = APIRouter()
        controller = RootController()
        router.add_api_route("/", controller.index, methods=["GET"])
        router.add_api_route("/download-collections", controller.download_collections, methods=["GET"])
        router.add_api_route("/health", controller.health_check, methods=["GET"])
        router.add_api_route("/health/db", controller.health_check_db, methods=["GET"])
        router.add_api_route("/health/redis", controller.health_check_redis, methods=["GET"])
        return router
