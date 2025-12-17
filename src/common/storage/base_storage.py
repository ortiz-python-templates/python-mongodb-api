from fastapi import UploadFile
from src.common.storage.upload_info import UploadInfo
from common.storage.storage_bucket import StorageBucket


class BaseStorage:
    """Interface/base class for any storage backend."""

    def upload(self, file: UploadFile, bucket: StorageBucket) -> UploadInfo:
        raise NotImplementedError

    def get_file_url(self, object_key: str, expires_in_seconds: int = 3600) -> str:
        raise NotImplementedError