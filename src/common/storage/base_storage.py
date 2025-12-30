from abc import ABC, abstractmethod
from io import BytesIO
from fastapi import UploadFile
from src.common.storage.storage_provider import StorageProvider
from src.common.storage.upload_info import UploadInfo


class BaseStorage(ABC):
    """Interface/base class for any storage backend."""

    provider_name: StorageProvider
    is_available: bool

    @abstractmethod
    async def upload(self, file: UploadFile, storage_path: str) -> UploadInfo:
        pass

    @abstractmethod
    async def download(self, object_key: str) -> BytesIO:
        pass

   
    def get_pressigned_url(self, object_key: str, expire_in_minutes: int = 60) -> str:
        pass
    
    def get_provider_name(self):
        return self.provider_name