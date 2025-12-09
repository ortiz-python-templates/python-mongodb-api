from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from src.core.seed.database_indexes import DatabaseIndexes
from src.core.seed.database_objects import DatabaseObjects
from src.core.seed.setup import SeedSetup
from src.common.config.db_config import DbConfig
from src.common.config.env_config import EnvConfig
from src.common.config.log_config import Logger  


class AppLifespan:

    @staticmethod
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        logger = Logger.get_logger("app.lifespan")

        #db = DbConfig.get_database()
        client = AsyncIOMotorClient(EnvConfig.MONGO_URI)  
        db = client[EnvConfig.MONGO_DATABASE]

        # Runs when the app starts
        logger.info("Starting application...")

        # Ensure indexes
        await DatabaseIndexes.setup_indexes(db)

        logger.info("Creating database views and objects...")
        await DatabaseObjects.create_views(db)

        logger.info("Seeding initial data...")
        await SeedSetup.seed_initial_data(db)

        yield  # App runs here

        # Runs when the app stops
        logger.info("Shutting down application...")
        client.close()
