import os
import uuid
from datetime import datetime
from typing import List
from fastapi import UploadFile
from src.common.storage.base_storage import BaseStorage
from src.common.config.env_config import EnvConfig
from src.common.storage.upload_info import UploadInfo


class FileSystemStorage(BaseStorage):
    """Service for uploading and managing files in the local file system."""

    def __init__(self):
        self.destination_path = EnvConfig.FILESYSTEM_STORAGE_PATH
        os.makedirs(self.destination_path, exist_ok=True)

    def upload(self, file: UploadFile, storage_path: str) -> UploadInfo:
        """Saves a single uploaded file to the file system."""
        if not file:
            raise ValueError("No file provided.")

        file_name = self._generate_unique_file_name(file.filename)
        size = self._save_uploaded_file(file, storage_path, file_name)

        return UploadInfo(
            original_file_name=file.filename,
            final_name=file_name,
            size=size,
            content_type=file.content_type,
            extension=os.path.splitext(file.filename)[1],
            upload_time=datetime.now()
        )

    def upload_multiple_files(self, files: List[UploadFile], storage_path: str) -> List[UploadInfo]:
        """Uploads multiple files and returns a list of UploadInfo objects."""
        if not files or len(files) == 0:
            raise ValueError("No files provided.")

        upload_infos: List[UploadInfo] = []

        for file in files:
            if not file:
                continue

            file_name = self._generate_unique_file_name(file.filename)
            size = self._save_uploaded_file(file, storage_path, file_name)

            upload_infos.append(UploadInfo(
                original_file_name=file.filename,
                final_name=file_name,
                size=size,
                content_type=file.content_type,
                extension=os.path.splitext(file.filename)[1],
                upload_time=datetime.now()
            ))

        return upload_infos

    def get_file_url(self, storage_path: str, file_name: str) -> str:
        """Generates a full path to the file stored locally."""
        return os.path.join(self.destination_path, storage_path, file_name)

    def _generate_unique_file_name(self, filename: str) -> str:
        """Generates a unique filename by appending a UUID."""
        return f"{uuid.uuid4()}{os.path.splitext(filename)[1]}"

    def _save_uploaded_file(self, file: UploadFile, storage_path: str, file_name: str) -> int:
        """Writes the uploaded file's binary content to disk and returns the file size."""
        full_path = os.path.join(self.destination_path, storage_path)
        os.makedirs(full_path, exist_ok=True)

        file_path = os.path.join(full_path, file_name)
        content = file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        return len(content)
