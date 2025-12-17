from fastapi import UploadFile
from src.common.storage.upload_info import UploadInfo
from src.common.storage.storage_bucket import StorageBucket


class BaseStorage:
    """Interface/base class for any storage backend."""

    def upload(self, file: UploadFile, bucket: StorageBucket) -> UploadInfo:
        raise NotImplementedError

    def get_pressigned_url(self, object_key: str, expire_in_minutes: int = 60) -> str:
        raise NotImplementedError