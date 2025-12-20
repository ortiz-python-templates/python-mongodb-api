from src.common.storage.base_storage import BaseStorage
from src.common.storage.filestystem_storage import FileSystemStorage
from src.common.storage.google_storage import GoogleStorage
from src.common.storage.minio_storage import MinioStorage
from src.common.config.env_config import EnvConfig
from common.storage.storage_provider import StorageProvider


class StorageProviderFactory:

    @classmethod
    def get_provider() -> BaseStorage:
        provider = EnvConfig.STORAGE_PROVIDER

        match provider:
            case StorageProvider.MINIO:
                return MinioStorage()
            case StorageProvider.GCS:
                return GoogleStorage()
            case StorageProvider.FILESYSTEM:
                return FileSystemStorage()
            case _:
                raise ValueError(f"Unsupported storage provider: {provider}")