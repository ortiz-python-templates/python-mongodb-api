from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.core.controllers.files.file_controller import FileController
from src.core.controllers.identity.user_attachment_controller import UserAttachmentController
from src.core.controllers.configurations.basic_configuration_controller import BasicConfigurationController
from src.core.controllers.configurations.company_configuration_controller import CompanyConfigurationController
from src.core.controllers.configurations.feature_flag_controller import FeatureFlagController
from src.core.controllers.identity.login_activity_controller import LoginActivityController
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
      app.include_router(UserAttachmentController.add_routes(db), prefix="/api/user-attachments", tags=["Identity / Users Attachments"])
      app.include_router(LoginActivityController.add_routes(db), prefix="/api/login-activities", tags=["Identity / Login Activities"])

      # Configurations ----------------------------------------------------------------------------------------------
      app.include_router(BasicConfigurationController.add_routes(db), prefix="/api/basic-configurations", tags=["Configurations / Basic Configurations"])
      app.include_router(CompanyConfigurationController.add_routes(db), prefix="/api/company-configurations", tags=["Configurations / Company Configurations"])
      app.include_router(FeatureFlagController.add_routes(db), prefix="/api/feature-flags", tags=["Configurations / Feature Flags"])

      # Files ----------------------------------------------------------------------------------------------
      app.include_router(FileController.add_routes(db), prefix="/api/files", tags=["Files"])
