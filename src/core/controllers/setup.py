from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.core.controllers._root.health_controller import HealthController
from src.core.controllers._root.root_controller import RootController
from src.core.controllers.identity.role_controller import RoleController
from src.core.controllers.identity.auth_controller import AuthController
from src.core.controllers.identity.user_controller import UserController


class ControllersSetup:
   
   def setup(app: FastAPI, db: AsyncIOMotorDatabase):
      
      # Root -------------------------------------------------------------------------------------------------
      app.include_router(RootController.add_routes(), tags=["API Root"])
      app.include_router(HealthController.add_routes(), tags=["API Health"])

      # Identity ----------------------------------------------------------------------------------------------
      app.include_router(AuthController.add_routes(db), prefix="/api/auth", tags=["Identity / Authentication"])
      app.include_router(RoleController.add_routes(), prefix="/api/roles", tags=["Identity / Roles"])
      app.include_router(UserController.add_routes(db), prefix="/api/users", tags=["Identity / Users"])
