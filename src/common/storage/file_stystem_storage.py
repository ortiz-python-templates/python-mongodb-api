import os
import uuid
from datetime import datetime
from typing import List
from fastapi import UploadFile
from src.common.storage.upload_info import UploadInfo


class FileSystemStorage:
    """Service for uploading and managing files in the local file system."""

    def __init__(self, destination_path: str, allowed_extensions: List[str], max_size: int):
        if not destination_path:
            raise ValueError("Destination path cannot be null or empty.")

        self.destination_path = destination_path
        self.allowed_extensions = [ext.lower() for ext in allowed_extensions]
        self.max_size = max_size

        # Create destination directory if it does not exist
        os.makedirs(self.destination_path, exist_ok=True)


    async def upload_single_file(self, file: UploadFile) -> UploadInfo:
        """Saves a single uploaded file to the file system."""
        if not file:
            raise ValueError("No file provided.")

        # Generate a unique name and save the file
        file_name = self._generate_unique_file_name(file.filename)
        await self._save_uploaded_file(file, file_name)

        return UploadInfo(
            original_file_name=file.filename,
            final_name=file_name,
            size=file.size if hasattr(file, "size") else 0,
            content_type=file.content_type,
            extension=os.path.splitext(file.filename)[1],
            upload_time=datetime.now()
        )


    async def upload_multiple_files(self, files: List[UploadFile]) -> List[UploadInfo]:
        """Uploads multiple files and returns a list of UploadInfo objects."""
        if not files or len(files) == 0:
            raise ValueError("No files provided.")

        upload_infos: List[UploadInfo] = []

        for file in files:
            if not file:
                continue

            file_name = self._generate_unique_file_name(file.filename)
            await self._save_uploaded_file(file, file_name)

            upload_infos.append(UploadInfo(
                original_file_name=file.filename,
                final_name=file_name,
                size=file.size if hasattr(file, "size") else 0,
                content_type=file.content_type,
                extension=os.path.splitext(file.filename)[1],
                upload_time=datetime.now()
            ))

        return upload_infos
    

    def get_file_url(self, file_name: str) -> str:
        """Generates a full URL or path to the file stored locally."""
        return os.path.join(self.destination_path, file_name)
    

    def _generate_unique_file_name(self, filename: str) -> str:
        """Generates a unique filename by appending a UUID."""
        return f"{uuid.uuid4()}{os.path.splitext(filename)[1]}"


    async def _save_uploaded_file(self, file: UploadFile, file_name: str):
        """Writes the uploaded file's binary content to disk."""
        file_path = os.path.join(self.destination_path, file_name)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
