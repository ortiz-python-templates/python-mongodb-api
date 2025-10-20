import uvicorn
from fastapi import FastAPI
from src.common.config.swagger_config import SwaggerConfig
from src.common.config.static_config import StaticConfig
from src.common.config.env_config import EnvConfig
from src.common.config.db_config import DbConfig
from src.common.middlewares.setup import MiddlewareSetup
from src.core.seed.app_lifespan import AppLifespan
from src.core.controllers.setup import ControllersSetup


# swagger config
app = FastAPI(**SwaggerConfig.config, lifespan=AppLifespan.lifespan)

# database connection
db = DbConfig.get_database()

# Static files
StaticConfig.setup(app)

# Middlewares 
MiddlewareSetup.setup(app, db)

# App routes
ControllersSetup.setup(app, db)


# start app
if __name__ == "__main__":
    print(f"Starting server on port {EnvConfig.PORT}")
    uvicorn.run(app,
        host=EnvConfig.app_host(), 
        port=EnvConfig.PORT,
        log_level="info"
    )