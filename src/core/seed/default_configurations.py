from src.core.repositories.configurations.company_configuration_command_repository import CompanyConfigurationCommandRepository
from src.core.repositories.configurations.basic_configuration_command_repository import BasicConfigurationCommandRepository
from src.core.models.configurations.basic_configuration_model import BasicConfigurationModel
from src.core.models.configurations.company_configuration_model import CompanyConfigurationModel
from src.common.config.log_config import Logger  
from motor.motor_asyncio import AsyncIOMotorDatabase


class DefaultConfigurations:


    @staticmethod
    async def seed_app_configurations(db: AsyncIOMotorDatabase):
        await DefaultConfigurations.seed_basic_configurations(db)
        await DefaultConfigurations.seed_company_configurations(db)


    @staticmethod
    async def seed_basic_configurations(db: AsyncIOMotorDatabase):
        logger = Logger.get_logger("seeder.basic_configurations")
        repository = BasicConfigurationCommandRepository(db)

        logger.info("Checking if Basic Configurations exist ...")
        current_config = await repository.get_last_aux()
        if current_config is None:
            logger.warning("Basic Configurations not found. Creating...")
            basic_config = BasicConfigurationModel(
                app_name="Python Template MongoDB API",
                app_acronym="mongo-db-api",
                max_records_per_page=100,
                max_admin_users=5,
                max_super_admin_users=2
            )
            await repository.create(basic_config)
            logger.warning("Basic Configurations created successfully.")
        else:
            logger.info("Basic Configurations already exist. Skipping...")


    @staticmethod
    async def seed_company_configurations(db: AsyncIOMotorDatabase):
        logger = Logger.get_logger("seeder.company_configurations")
        repository = CompanyConfigurationCommandRepository(db)

        logger.info("Checking if Company Configurations exist ...")
        current_config = await repository.get_last_aux()
        if current_config is None:
            logger.warning("Company Configurations not found. Creating...")
            company_config = CompanyConfigurationModel(
                name="Company 01",
                acronym="cp-01",
                ident_number="ID-01",
                email="company-mail@info.com",
                phone="(244)923 123 456",
                address="Company address"
            )
            await repository.create(company_config)
            logger.warning("Company Configurations created successfully.")
        else:
            logger.info("Company Configurations already exist. Skipping...")
