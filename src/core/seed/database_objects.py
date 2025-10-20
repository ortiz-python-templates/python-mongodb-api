import json
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import CollectionInvalid
from src.common.config.env_config import EnvConfig
from src.common.config.log_config import Logger  


class DatabaseObjects:
    
    @staticmethod
    async def create_views(db: AsyncIOMotorDatabase):
        logger = Logger.get_logger("database.views")

        # Base path where module view files are stored
        base_path = Path(__file__).resolve().parent.parent.parent.parent / "database" / "views"

        if not base_path.exists():
            logger.error(f"Views folder not found: {base_path}")
            return

        # Detect current environment
        environment = EnvConfig.ENVIRONMENT
        is_dev = environment in ["dev", "development", "local"]
        logger.info(f"Environment: {environment} | Recreate views: {is_dev}")

        # Get existing collections (avoid multiple DB calls)
        existing_collections = await db.list_collection_names()

        # Search for all JSON view definitions in subfolders
        for view_file in base_path.rglob("view_*.json"):
            view_name = view_file.stem

            try:
                if view_name in existing_collections:
                    info = await db.command("listCollections", filter={"name": view_name})
                    coll_type = info["cursor"]["firstBatch"][0].get("type", "collection")

                    if coll_type == "view":
                        if is_dev:
                            db[view_name].drop()
                            logger.info(f"View '{view_name}' removed for recreation.")
                        else:
                            logger.warning(f"View '{view_name}' already exists. Skipping (production).")
                            continue
                    else:
                        logger.warning(f"'{view_name}' already exists as a normal collection. Skipping.")
                        continue

                # Read the file only if we are creating or recreating the view
                with open(view_file, encoding="utf-8") as f:
                    data = json.load(f)

                # Create the view
                await db.create_collection(
                    name=view_name,
                    viewOn=data["viewOn"],
                    pipeline=data["pipeline"]
                )
                logger.info(f"View '{view_name}' created successfully.")

            except CollectionInvalid as e:
                logger.error(f"Error creating view '{view_name}': {e}")
            except Exception as e:
                logger.exception(f"Unexpected error creating view '{view_name}' in '{view_file}': {e}")
                raise
