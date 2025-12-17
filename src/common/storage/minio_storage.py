import uuid
from datetime import datetime, timedelta
from minio import Minio
from fastapi import UploadFile
from src.common.config.env_config import EnvConfig
from src.common.storage.upload_info import UploadInfo
from src.common.storage.units_of_measurement import UnitsOfMeasurement


class MinioStorage:
    """
    MinIO storage service.
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

        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)


    def upload(self, file: UploadFile, prefix: str) -> UploadInfo:
        """
        Uploads a file to MinIO under a logical prefix (folder).
        """
        object_key = f"{prefix}/{uuid.uuid4()}_{file.filename}"

        self.client.put_object(
            bucket_name=self.bucket_name,
            object_name=object_key,
            data=file.file,
            length=-1,
            part_size=10 * UnitsOfMeasurement.MEGA_BYTE
        )

        # file size
        file.file.seek(0, 2)
        size_bytes = file.file.tell()
        file.file.seek(0)

        file_url = self.get_file_url(object_key)

        return UploadInfo(
            file_name=file.filename,
            file_size=str(size_bytes),
            content_type=file.content_type or "application/octet-stream",
            metadata={
                "uploaded_at": datetime.utcnow().isoformat() + "Z"
            },
            object_key=object_key,
            file_url=file_url
        )


    def get_file_url(self, object_key: str, expires_in_seconds: int = 3600) -> str:
        return self.client.presigned_get_object(
            bucket_name=self.bucket_name,
            object_name=object_key,
            expires=timedelta(seconds=expires_in_seconds)
        )
