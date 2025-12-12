from datetime import datetime
from fastapi import Request
from src.core.schemas.configurations.basic_configuration_responses import BasicConfigurationDetail
from src.core.repositories.configurations.basic_configuration_query_repository import BasicConfigurationQueryRepository
from src.common.utils.messages.configurations_messages import BasicConfigMsg
from src.core.schemas.common_results import UpdatedResult
from src.core.schemas.configurations.basic_configuration_requests import UpdateBasicConfigurationRequest
from src.core.repositories.configurations.basic_configuration_command_repository import BasicConfigurationCommandRepository


class BasicConfigurationService:

    def __init__(self, db):
        self.command_repository = BasicConfigurationCommandRepository(db)
        self.query_repository = BasicConfigurationQueryRepository(db)


    async def update_basic_configuration(self, request: Request, body: UpdateBasicConfigurationRequest):
        configuration = await self.command_repository.get_last_aux()
        # current user
        current_user = request.state.user
        # update
        configuration.app_name =  body.app_name
        configuration.app_acronym = body.app_acronym
        configuration.max_records_per_page = body.max_records_per_page
        configuration.max_admin_users = body.max_admin_users
        configuration.max_super_admin_users = body.max_super_admin_users
        configuration.updated_at = datetime.now()
        configuration.updated_by = current_user.id
        await self.command_repository.update(configuration.id, configuration)
        
        return UpdatedResult(
            id=configuration.unique_id,
            message=BasicConfigMsg.Success.UPDATED
        )
    
    async def get_basic_configurations(self, request: Request):
        configuration = await self.query_repository.get_last()
        if configuration is None:
            return BasicConfigurationDetail(id="")
        return configuration