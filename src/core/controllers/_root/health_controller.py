from fastapi import APIRouter
from fastapi.responses import JSONResponse
import time
import socket
import psutil
from datetime import datetime
from src.common.config.db_config import DbConfig
from src.common.config.redis_client import RedisClient
from src.common.config.env_config import EnvConfig


START_TIME = time.time()

async def mongo_health():
    start = time.time()
    try:
        db = DbConfig.get_database()
        await db.command("ping")
        return {"status": "up", "latency_ms": round((time.time() - start) * 1000, 2)}
    except Exception:
        return {"status": "down"}


async def redis_health():
    start = time.time()
    try:
        await RedisClient._redis.ping()
        return {"status": "up", "latency_ms": round((time.time() - start) * 1000, 2)}
    except Exception:
        return {"status": "down"}


class HealthController:

    def __init__(self):
        pass

    async def health_liveness(self):
        return JSONResponse({
            "status": "ok",
            "service": EnvConfig.APP_NAME,
            "timestamp": datetime.now().isoformat() + "Z"
        })

    
    async def health_readiness(self):
        mongo = await mongo_health()
        redis = await redis_health()
        is_ready = mongo["status"] == "up" and redis["status"] == "up"

        return JSONResponse(
            {
                "status": "ok" if is_ready else "error",
                "dependencies": {
                    "mongodb": mongo,
                    "redis": redis
                }
            },
            status_code=200 if is_ready else 503
        )


    async def health_check(self):
        uptime = int(time.time() - START_TIME)

        mongo = await mongo_health()
        redis = await redis_health()

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
            "timestamp": datetime.now().isoformat() + "Z",
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