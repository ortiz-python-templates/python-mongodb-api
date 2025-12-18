from datetime import datetime
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from src.common.config.env_config import EnvConfig
from src.common.config.log_config import Logger
from src.common.config.redis_client import RedisClient
from src.core.bootstrap.database_indexes import DatabaseIndexes
from src.core.bootstrap.database_objects import DatabaseObjects
from src.core.bootstrap.setup import SeedSetup


class AppLifespan:

    @staticmethod
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        logger = Logger.get_logger("app.lifespan")
        app.state.start_time = datetime.now()

        logger.info("Starting application...")

        # Connect to MongoDB 
        try:
            mongo_client = AsyncIOMotorClient(EnvConfig.MONGO_URI, serverSelectionTimeoutMS=5000)
            db = mongo_client[EnvConfig.MONGO_DATABASE]
            await db.client.admin.command("ping")
            app.state.db = db
            logger.info("MongoDB connection successful.")
        except Exception as e:
            logger.error(f"MongoDB connection failed: {e}")
            raise RuntimeError("Cannot start application without MongoDB.") from e

        # Connect to Redis 
        try:
            await RedisClient.init()
            pong = await RedisClient.get("health_check")
            app.state.redis_available = True
            logger.info("Redis connection successful.")
        except Exception as e:
            app.state.redis_available = False
            logger.warning(f"Redis not available: {e}")

        # Setup indexes, views, and seed initial data
        try:
            await DatabaseIndexes.setup_indexes(db)
            await DatabaseObjects.create_views(db)
            await SeedSetup.seed_initial_data(db)
            logger.info("Database setup completed.")
        except Exception as e:
            logger.error(f"Database setup failed: {e}")
            raise RuntimeError("Cannot initialize database properly.") from e

        yield  # Application runs here

        # Shutdown tasks
        logger.info("Shutting down application...")
        mongo_client.close()
        if getattr(app.state, "redis_available", False):
            logger.info("Redis cleanup complete.")
