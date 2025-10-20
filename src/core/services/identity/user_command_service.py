from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.common.mail.email_service import EmailService
from src.common.utils.encryption_util import EncryptionUtil
from src.common.utils.password_util import PasswordUtil
from src.core.models.identity.user_model import UserModel
from src. common.utils.custom_exceptions import *
from src.core.schemas.identity.user_requests import *
from src.core.repositories.identity.user_command_repository import UserCommandRepository


class UserCommandService:

    def __init__(self, db: AsyncIOMotorDatabase):
        self.command_repository = UserCommandRepository(db)
        self.email_service = EmailService()


    async def create_user(self, body: CreateUserRequest):
        if await self.command_repository.exists_record('email', body.email):
            raise ConflictException(f"Já existe um usuário com o email '{body.email}'.")
        new_user = UserModel(
            email=body.email,
            role=body.role,
            first_name=body.first_name,
            last_name=body.last_name,
            password=PasswordUtil.hash(body.password),
            recovery_token=EncryptionUtil.generate_random_token(32),
            is_active=True
        )
        user_id = await self.command_repository.create(new_user)
        if user_id is None:
            raise InternalServerErrorException("Não foi possível criar o usuário. Verifique os dados e tente novamente.")
        # send email
        await self.email_service.send_email(
            subject="Registo de Usuário",
            email_to=body.email,
            template_name="email/user-registration.html",
            context={
                "user_full_name": f"{new_user.first_name} {new_user.last_name}",
                "user_email": new_user.email,
                "user_password": body.password
            }
        )
        return user_id
    

    async def update_user(self, unique_id: str, body: UpdateUserRequest):
        user = await self.command_repository.get_by_unique_id_aux(unique_id)
        if user is None:
            raise NotFoundException(f"Não encontramos nenhum usuário com o ID '{unique_id}'.")
        user.first_name = body.first_name
        user.last_name = body.last_name
        user.updated_at = datetime.now()
        self.command_repository.update(user.id, user)


    async def activate_user(self, unique_id: str, body: ActivateUserRequest):
        user = await self.command_repository.get_by_unique_id_aux(unique_id)
        if user is None:
            raise NotFoundException(f"Não encontramos nenhum usuário com o ID '{unique_id}'.")
        if user.is_active == True:
            raise ConflictException(f"Usuário com ID '{unique_id}' já está activo")
        user.is_active = True
        user.updated_at = datetime.now()
        self.command_repository.update(user.id, user)
        # send email
        await self.email_service.send_email(
            subject="Status do usuário",
            email_to=user.email,
            template_name="email/change-user-status.html",
            context={
                "user_email": user.email,
                "user_status": "Activado",
                "status_reason": body.reason
            }
        )


    async def deactivate_user(self, unique_id: str, body: DeactivateUserRequest):
        user = await self.command_repository.get_by_unique_id_aux(unique_id)
        if user is None:
           raise NotFoundException(f"Não encontramos nenhum usuário com o ID '{unique_id}'.")
        if user.is_active == False:
            raise ConflictException(f"Usuário com ID '{unique_id}' já está inactivo")
        user.is_active = False
        user.updated_at = datetime.now()
        await self.command_repository.update(user.id, user)
        # send email
        await self.email_service.send_email(
            subject="Status do usuário",
            email_to=user.email,
            template_name="email/change-user-status.html",
            context={
                "user_email": user.email,
                "user_status": "Desactivado",
                "status_reason": body.reason
            }
        )


    async def register_user(self, body: RegisterUserRequest):
        if await self.command_repository.exists_record('email', body.email):
            raise ConflictException(f"Email '{body.email}' já existe")
        new_user = UserModel(
            email=body.email,
            first_name=body.first_name,
            last_name=body.last_name,
            profile_completed=False,
            password=PasswordUtil.hash(body.password),
            recovery_token=EncryptionUtil.generate_random_token(32),
            is_active=True
        )
        inserted_id = await self.command_repository.create(new_user)
        if inserted_id is None:
            raise InternalServerErrorException("Não foi possível registrar o usuário. Por favor, tente novamente.")
        # send email
        await self.email_service.send_email(
            subject="Registo de Usuário",
            email_to=body.email,
            template_name="email/user-registration.html",
            context={
                "user_full_name": f"{new_user.first_name} {new_user.last_name}",
                "user_email": new_user.email,
                "user_password": body.password
            }
        )
        return inserted_id



