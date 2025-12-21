from io import BytesIO
import uuid
from datetime import datetime, timezone, timedelta
from minio import Minio, S3Error
from fastapi import UploadFile
from src.common.storage.storage_provider import StorageProvider
from src.common.storage.base_storage import BaseStorage
from src.common.config.env_config import EnvConfig
from src.common.storage.upload_info import UploadInfo
from src.common.storage.units_of_measurement import UnitsOfMeasurement


class MinioStorage(BaseStorage):
    """
    MinIO storage service.
    Implements BaseStorage interface. Uses bucket + object_key prefixes to simulate folders.
    Does not break if MinIO is unavailable.
    """

    def __init__(self):
        self.is_available = True
        try:
            self.client = Minio(
                EnvConfig.MINIO_ENDPOINT,
                access_key=EnvConfig.MINIO_ROOT_USER,
                secret_key=EnvConfig.MINIO_ROOT_PASSWORD,
                secure=EnvConfig.minio_secure()
            )
            self.provider_name = StorageProvider.MINIO
            self.bucket_name = EnvConfig.MINIO_MAIN_BUCKET
            self._ensure_bucket()
        except Exception as e:
            # Storage not available, log warning and mark unavailable
            print(f"[x] MinIO storage not available: {e}")
            self.is_available = False


    def _ensure_bucket(self):
        """Ensure the main bucket exists."""
        if not self.is_available:
            return
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
        except S3Error as e:
            print(f"[x] Failed to ensure bucket '{self.bucket_name}': {e}")
            self.is_available = False


    async def upload(self, file: UploadFile, storage_path: str) -> UploadInfo:
        if not self.is_available:
            raise RuntimeError("MinIO storage is not available.")

        object_key = f"{storage_path}/{uuid.uuid4()}_{file.filename}"

        try:
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=object_key,
                data=file.file,
                length=-1,  # streaming
                part_size=10 * UnitsOfMeasurement.MEGA_BYTE
            )
        except S3Error as e:
            raise RuntimeError(f"Failed to upload file '{file.filename}': {e}")

        # Calculate file size safely
        try:
            file.file.seek(0, 2)
            size_bytes = file.file.tell()
            file.file.seek(0)
        except Exception:
            size_bytes = 0

        file_url = self.get_pressigned_url(object_key)

        metadata = {
            "uploaded_at": datetime.now(timezone.utc).isoformat() + "Z"
        }

        return UploadInfo(
            file_name=file.filename,
            file_size=str(size_bytes),
            content_type=file.content_type or "application/octet-stream",
            metadata=metadata,
            object_key=object_key,
            file_url=file_url
        )
    

    async def download(self, object_key: str) -> BytesIO:
        if not self.is_available:
            raise RuntimeError("MinIO storage is not available.")

        try:
            response = self.client.get_object(bucket_name=self.bucket_name, object_name=object_key)
            data = response.read()
            response.close()
            response.release_conn()
            return BytesIO(data)
        except S3Error as e:
            raise RuntimeError(f"Failed to download file '{object_key}': {e}")


    def get_pressigned_url(self, object_key: str, expire_in_minutes: int = 60) -> str:
        if not self.is_available:
            return ""
        try:
            return self.client.presigned_get_object(
                bucket_name=self.bucket_name,
                object_name=object_key,
                expires=timedelta(minutes=expire_in_minutes)
            )
        except S3Error as e:
            print(f"[x] Failed to generate URL for '{object_key}': {e}")
            return ""


    def get_permanent_url(self, storage_path: str, object_key: str) -> str:
        if not self.is_available:
            return ""
        try:
            return f"{EnvConfig.MINIO_ENDPOINT}/{storage_path}/{object_key}"
        except S3Error as e:
            print(f"[x] Failed to generate permanent URL: {e}")
            return ""
