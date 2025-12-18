from datetime import datetime
from fastapi import Request
from src.core.schemas.configurations.company_configuration_responses import CompanyConfigurationDetail
from src.core.repositories.configurations.company_configuration_query_repository import CompanyConfigurationQueryRepository
from src.core.schemas.configurations.basic_configuration_responses import BasicConfigurationDetail
from src.common.utils.messages.configurations_messages import CompanyConfigMsg
from src.core.schemas.common_results import UpdatedResult
from src.core.schemas.configurations.company_configuration_requests import UpdateCompanyConfigurationRequest
from src.core.repositories.configurations.company_configuration_command_repository import CompanyConfigurationCommandRepository


class CompanyConfigurationService:

    def __init__(self, db):
        self.command_repository = CompanyConfigurationCommandRepository(db)
        self.query_repository = CompanyConfigurationQueryRepository(db)


    async def update_company_configuration(self, request: Request, body: UpdateCompanyConfigurationRequest):
        configuration = await self.command_repository.get_last_aux()
        # current user
        current_user = request.state.user
        # update
        configuration.name = body.name
        configuration.acronym = body.acronym
        configuration.address = body.address
        configuration.email = body.email
        configuration.identification_number =  body.identification_number
        configuration.updated_at = datetime.now()
        configuration.updated_by = current_user.id
        await self.command_repository.update(configuration.id, configuration)
        
        return UpdatedResult(
            id=configuration.unique_id,
            message=CompanyConfigMsg.Success.UPDATED
        )
    
        
    async def get_company_configurations(self, request: Request) -> CompanyConfigurationDetail:
        configuration = await self.query_repository.get_last()
        if configuration is None:
            return CompanyConfigurationDetail(id="")
        return configuration