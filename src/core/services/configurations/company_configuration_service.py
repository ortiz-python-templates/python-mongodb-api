from datetime import datetime
from fastapi import Request
from src.core.schemas.common_result import UpdatedResult
from src.core.schemas.configurations.company_configuration_requests import UpdateCompanyConfigurationRequest
from src.core.repositories.configurations.company_configuration_command_repository import CompanyConfigurationCommandRepository


class CompanyConfigurationCommandService:

    def __init__(self, db):
        self.command_repository = CompanyConfigurationCommandRepository(db)


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
            message="Company configurations updated"
        )