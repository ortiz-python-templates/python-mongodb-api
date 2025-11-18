from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.common.mail.email_service import EmailService
from src.common.utils.encryption_util import EncryptionUtil
from src.common.utils.password_util import PasswordUtil
from src.core.models.identity.user_model import UserModel
from src.common.utils.custom_exceptions import *
from src.core.schemas.identity.user_requests import *
from src.core.repositories.identity.user_command_repository import UserCommandRepository


class UserCommandService:

    def __init__(self, db: AsyncIOMotorDatabase):
        self.command_repository = UserCommandRepository(db)
        self.email_service = EmailService()


    async def create_user(self, body: CreateUserRequest):
        if await self.command_repository.exists_record('email', body.email):
            raise ConflictException(f"A user with email '{body.email}' already exists.")
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
            raise InternalServerErrorException("Unable to create user. Please check the data and try again.")
        # send email
        await self.email_service.send_email(
            subject="User Registration",
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
            raise NotFoundException(f"No user found with ID '{unique_id}'.")
        user.first_name = body.first_name
        user.last_name = body.last_name
        user.updated_at = datetime.now()
        self.command_repository.update(user.id, user)


    async def activate_user(self, unique_id: str, body: ActivateUserRequest):
        user = await self.command_repository.get_by_unique_id_aux(unique_id)
        if user is None:
            raise NotFoundException(f"No user found with ID '{unique_id}'.")
        if user.is_active:
            raise ConflictException(f"User with ID '{unique_id}' is already active.")
        user.is_active = True
        user.updated_at = datetime.now()
        self.command_repository.update(user.id, user)
        # send email
        await self.email_service.send_email(
            subject="User Status Update",
            email_to=user.email,
            template_name="email/change-user-status.html",
            context={
                "user_email": user.email,
                "user_status": "Activated",
                "status_reason": body.reason
            }
        )


    async def deactivate_user(self, unique_id: str, body: DeactivateUserRequest):
        user = await self.command_repository.get_by_unique_id_aux(unique_id)
        if user is None:
           raise NotFoundException(f"No user found with ID '{unique_id}'.")
        if not user.is_active:
            raise ConflictException(f"User with ID '{unique_id}' is already inactive.")
        user.is_active = False
        user.updated_at = datetime.now()
        await self.command_repository.update(user.id, user)
        # send email
        await self.email_service.send_email(
            subject="User Status Update",
            email_to=user.email,
            template_name="email/change-user-status.html",
            context={
                "user_email": user.email,
                "user_status": "Deactivated",
                "status_reason": body.reason
            }
        )


    async def register_user(self, body: RegisterUserRequest):
        if await self.command_repository.exists_record('email', body.email):
            raise ConflictException(f"Email '{body.email}' already exists.")
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
            raise InternalServerErrorException("Unable to register user. Please try again.")
        # send email
        await self.email_service.send_email(
            subject="User Registration",
            email_to=body.email,
            template_name="email/user-registration.html",
            context={
                "user_full_name": f"{new_user.first_name} {new_user.last_name}",
                "user_email": new_user.email,
                "user_password": body.password
            }
        )
        return inserted_id
