from fastapi import UploadFile
from src.common.storage.upload_info import UploadInfo


class BaseStorage:
    """Interface/base class for any storage backend."""

    def upload(self, file: UploadFile, storage_path: str) -> UploadInfo:
        raise NotImplementedError

    def get_pressigned_url(self, object_key: str, expire_in_minutes: int = 60) -> str:
        raise NotImplementedError