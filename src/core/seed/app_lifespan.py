from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from src.core.seed.database_objects import DatabaseObjects
from src.common.config.db_config import DbConfig
from src.core.seed.setup import SeedSetup
from src.common.config.log_config import Logger  


class AppLifespan:

    @staticmethod
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        logger = Logger.get_logger("app.lifespan")

        db = DbConfig.get_database()

        # Runs when the app starts
        logger.info("Starting application...")
        logger.info("Creating database views and objects...")
        await DatabaseObjects.create_views(db)

        logger.info("Seeding initial data...")
        await SeedSetup.seed_initial_data(db)

        yield  # App runs here

        # Runs when the app stops
        logger.info("Shutting down application...")
