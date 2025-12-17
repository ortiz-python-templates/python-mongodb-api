import uuid
from datetime import datetime, timedelta
from minio import Minio, S3Error
from fastapi import UploadFile
from src.common.storage.base_storage import BaseStorage
from src.common.storage.storage_bucket import StorageBucket
from src.common.config.env_config import EnvConfig
from src.common.storage.upload_info import UploadInfo
from src.common.storage.units_of_measurement import UnitsOfMeasurement


class MinioStorage(BaseStorage):
    """
    MinIO storage service.
    Implements BaseStorage interface.
    Uses bucket + object_key prefixes to simulate folders.
    """

    def __init__(self):
        self.client = Minio(
            EnvConfig.MINIO_ENDPOINT,
            access_key=EnvConfig.MINIO_ROOT_USER,
            secret_key=EnvConfig.MINIO_ROOT_PASSWORD,
            secure=EnvConfig.minio_secure()
        )
        self.bucket_name = EnvConfig.MINIO_MAIN_BUCKET
        self._ensure_bucket()


    def _ensure_bucket(self):
        """Ensure the main bucket exists."""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
        except S3Error as e:
            raise RuntimeError(f"Failed to ensure bucket '{self.bucket_name}': {e}")


    def upload(self, file: UploadFile, bucket: StorageBucket) -> UploadInfo:
        """
        Uploads a file to MinIO under a logical prefix (folder) and returns UploadInfo.
        """
        object_key = f"{bucket.value}/{uuid.uuid4()}_{file.filename}"

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
            size_bytes = 0  # fallback if not seekable

        file_url = self.get_file_url(object_key)

        metadata = {
            "uploaded_at": datetime.utcnow().isoformat() + "Z"
        }

        return UploadInfo(
            file_name=file.filename,
            file_size=str(size_bytes),
            content_type=file.content_type or "application/octet-stream",
            metadata=metadata,
            object_key=object_key,
            file_url=file_url
        )


    def get_file_url(self, object_key: str, expires_in_seconds: int = 3600) -> str:
        """Generate a presigned URL for an existing object in MinIO."""
        try:
            return self.client.presigned_get_object(
                bucket_name=self.bucket_name,
                object_name=object_key,
                expires=timedelta(seconds=expires_in_seconds)
            )
        except S3Error as e:
            raise RuntimeError(f"Failed to generate URL for '{object_key}': {e}")
