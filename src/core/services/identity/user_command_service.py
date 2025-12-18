from datetime import datetime
from bson import ObjectId
from fastapi import Request, UploadFile
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.common.storage.storage_bucket import StorageBucket
from src.common.storage.minio_storage import MinioStorage
from src.common.utils.messages.identity_messsages import UserMsg
from src.core.schemas.common_results import *
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
        self.minio_storage = MinioStorage()


    async def create_user(self, request: Request, body: CreateUserRequest):
        if await self.command_repository.exists_record('email', body.email):
            raise ConflictException(f"A user with email '{body.email}' already exists.")
        current_user = request.state.user
        new_user = UserModel(
            email=body.email,
            role=body.role,
            first_name=body.first_name,
            last_name=body.last_name,
            password=PasswordUtil.hash(body.password),
            recovery_token=EncryptionUtil.generate_random_token(32),
            is_active=True,
            created_by=current_user.id
        )
        user_id = await self.command_repository.create(new_user)
        if user_id is None:
            raise InternalServerErrorException("Unable to create user. Please check the data and try again.")
        # send email
        await self.email_service.send_email(
            subject="User Registration",
            email_to=body.email,
            template_name="email/user-creation.html",
            context={
                "user_full_name": f"{new_user.first_name} {new_user.last_name}",
                "user_email": new_user.email,
                "user_password": body.password
            }
        )
        return CreatedResult(
            id=new_user.unique_id,
            message=UserMsg.Success.CREATED.format(body.email)
        )
    

    async def update_user(self, request: Request, unique_id: str, body: UpdateUserRequest):
        user = await self.command_repository.get_by_unique_id_aux(unique_id)
        if user is None:
            raise NotFoundException(f"No user found with ID '{unique_id}'.")
        current_user = request.state.user
        user.first_name = body.first_name
        user.last_name = body.last_name
        user.updated_at = datetime.now()
        user.updated_by = current_user.id
        self.command_repository.update(user.id, user)
        return UpdatedResult(
            id=unique_id,
            message=UserMsg.Success.UPDATED
        )


    async def activate_user(self, request: Request, unique_id: str, body: ActivateUserRequest):
        user = await self.command_repository.get_by_unique_id_aux(unique_id)
        if user is None:
            raise NotFoundException(f"No user found with ID '{unique_id}'.")
        if user.is_active:
            raise ConflictException(f"User with ID '{unique_id}' is already active.")
        current_user = request.state.user
        user.is_active = True
        user.updated_at = datetime.now()
        user.updated_by = current_user.id
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
        return UpdatedResult(
            id=unique_id,
            message=UserMsg.Success.ACTIVATED.format(unique_id)
        )


    async def deactivate_user(self, request: Request, unique_id: str, body: DeactivateUserRequest):
        user = await self.command_repository.get_by_unique_id_aux(unique_id)
        if user is None:
           raise NotFoundException(f"No user found with ID '{unique_id}'.")
        if not user.is_active:
            raise ConflictException(f"User with ID '{unique_id}' is already inactive.")
        current_user = request.state.user
        user.is_active = False
        user.updated_at = datetime.now()
        user.updated_by = current_user.id
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
        return UpdatedResult(
            id=unique_id,
            message=UserMsg.Success.DEACTIVATED.format(unique_id)
        )


    async def register_user(self, request: Request, body: RegisterUserRequest):
        if await self.command_repository.exists_record('email', body.email):
            raise ConflictException(f"Email '{body.email}' already exists.")
        new_user = UserModel(
            email=body.email,
            first_name=body.first_name,
            last_name=body.last_name,
            profile_completed=False,
            password=PasswordUtil.hash(body.password),
            recovery_token=EncryptionUtil.generate_random_token(32),
            is_active=True,
            created_by=None
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
        return CreatedResult(
            id=new_user.unique_id,
            message=UserMsg.Success.CREATED.format(body.email)
        )
    

    async def change_password(self, token: str, body: ChangePasswordRequest):
        user = await self.command_repository.get_by_recovery_token_aux(token)
        if not user:
            raise BadRequestException("Invalid or expired recovery token.")
        if not user.is_active:
            raise BadRequestException("Your account is currently inactive. Please contact support to reactivate it.")
        user.password = PasswordUtil.hash(body.new_password)
        user.recovery_token = EncryptionUtil.generate_random_token(32)
        self.command_repository.update(user.id, user)
         # send email
        await self.email_service.send_email(
            subject="Password Reset",
            email_to=user.email,
            template_name="email/change-password.html",
            context={
                "user_email": user.email,
                "new_password": body.new_password,
            }
        )
        return UpdatedResult(
            id=user.unique_id,
            message=UserMsg.Success.PASSWORD_CHANGED.format(user.unique_id)
        )


    async def update_user_avatar(self, request: Request, user_id: str, file: UploadFile):
        user = await self.get_user_by_unique_id_aux(user_id)
        current_user = request.state.user
        # upload
        upload_info = self.minio_storage.upload(file, StorageBucket.USER_AVATARS)
        # updatet user
        user.avatar_url = self.minio_storage.get_pressigned_url(upload_info.object_key)
        user.updated_at = datetime.now()
        user.updated_by = current_user.id
        return UpdatedResult(
            id=user.unique_id,
            message=UserMsg.Success.AVATAR_UPDATED.format(user.unique_id)
        )
    

    # aux query methods only to return UserModel avoiding mixture query and command repos
    async def get_user_by_email_aux(self, email: str) -> UserModel:
        user = await self.command_repository.get_by_email_aux(email)
        if user is None:
            raise NotFoundException("The provided email does not exists.")
        return user
    
    async def get_user_by_unique_id_aux(self, unique_id: str) -> UserModel:
        user = await self.command_repository.get_by_unique_id_aux(unique_id)
        if user is None:
            raise NotFoundException(f"User with ID '{unique_id}' does not exists.")
        return user
    
    async def get_user_by_recovery_token(self, token: str) -> UserModel:
        user = await self.command_repository.get_by_recovery_token_aux(token)
        if user is None:
            raise NotFoundException("The provided recovery token is invalid or has expired.")
        return user
   

    async def authenticate_user(self, email: str, password: str) -> UserModel:
        if not email or not password:
            raise BadRequestException("Please provide email and password to continue.")
        user = await self.command_repository.get_by_email_aux(email)
        if not user or not PasswordUtil.verify(password, user.password):
            raise UnauthorizedException("Incorrect email or password. Please try again.")
        return user

