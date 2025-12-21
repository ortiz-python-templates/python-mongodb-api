from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
import time
import socket
import psutil
from datetime import datetime, timezone
from src.core.services._root.health_service import HealthService
from src.common.config.env_config import EnvConfig


START_TIME = time.time()

class HealthController:

    def __init__(self):
        pass
    
    # livenes
    async def health_liveness(self):
        return JSONResponse({
            "status": "ok",
            "service": EnvConfig.APP_NAME,
            "timestamp": datetime.now(timezone.utc).isoformat() + "Z"
        })

    # readynes
    async def health_readiness(self):
        mongo = await HealthService.mongo_health()
        redis = await HealthService.redis_health()
        is_ready = mongo["status"] == "up" and redis["status"] == "up"

        return JSONResponse({
                "status": "ok" if is_ready else "error",
                "dependencies": {
                    "mongodb": mongo,
                    "redis": redis
                }
            },
            status_code=status.HTTP_200_OK if is_ready else status.HTTP_503_SERVICE_UNAVAILABLE
        )

    # complete check
    async def health_check(self):
        uptime = int(time.time() - START_TIME)

        mongo = await HealthService.mongo_health()
        redis = await HealthService.redis_health()

        overall_status = (
            "ok" if mongo["status"] == "up" and redis["status"] == "up" else "error"
        )

        process = psutil.Process()
        mem_info = process.memory_info()

        return JSONResponse({
            "status": overall_status,
            "service": EnvConfig.APP_NAME,
            "version": EnvConfig.APP_VERSION,
            "environment": EnvConfig.APP_ENVIRONMENT,
            "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
            "uptime_seconds": uptime,
            "hostname": socket.gethostname(),
            "dependencies": {
                "mongodb": mongo,
                "redis": redis,
            },
            "runtime": {
                "cpu_percent": psutil.cpu_percent(),
                "memory_rss_mb": round(mem_info.rss / (1024 * 1024), 2),
                "memory_vms_mb": round(mem_info.vms / (1024 * 1024), 2),
            }
        })
    

    @classmethod
    def add_routes(cls) -> APIRouter:
        router = APIRouter()
        controller = HealthController()
        router.add_api_route("/health", controller.health_check, methods=["GET"])
        router.add_api_route("/health/live", controller.health_liveness, methods=["GET"])
        router.add_api_route("/health/ready", controller.health_readiness, methods=["GET"])
        return router