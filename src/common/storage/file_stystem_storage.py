import os
import uuid
from datetime import datetime
from typing import List
from fastapi import UploadFile

from src.common.storage.upload_info import UploadInfo


class FileSystemStorage:
    def __init__(self, destination_path: str, allowed_extensions: List[str], max_size: int):
        if not destination_path:
            raise ValueError("DestinationPath cannot be null or empty.")

        self.destination_path = destination_path
        self.allowed_extensions = [ext.lower() for ext in allowed_extensions]
        self.max_size = max_size

        # Cria pasta se não existir
        os.makedirs(self.destination_path, exist_ok=True)

    async def upload_single_file(self, file: UploadFile) -> UploadInfo:
        if not file:
            raise ValueError("No file provided.")

        await self._validate_file(file)

        file_name = self._generate_unique_file_name(file.filename)
        await self._save_uploaded_file(file, file_name)

        return UploadInfo(
            original_file_name=file.filename,
            final_name=file_name,
            size=file.size if hasattr(file, "size") else 0,
            content_type=file.content_type,
            extension=os.path.splitext(file.filename)[1],
            upload_time=datetime.utcnow()
        )

    async def upload_multiple_files(self, files: List[UploadFile]) -> List[UploadInfo]:
        if not files or len(files) == 0:
            raise ValueError("No files provided.")

        upload_infos: List[UploadInfo] = []

        for file in files:
            if not file:
                continue

            await self._validate_file(file)
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
    
    def get_file_url(self):
        pass

    async def _validate_file(self, file: UploadFile):
        # Validar extensão
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in self.allowed_extensions:
            raise ValueError(
                f"File '{file.filename}' has an invalid extension. "
                f"Allowed extensions: {', '.join(self.allowed_extensions)}"
            )

        # Validar tamanho (precisa ler o ficheiro para saber o tamanho)
        file.file.seek(0, os.SEEK_END)
        size = file.file.tell()
        file.file.seek(0)

        if size > self.max_size:
            raise ValueError(
                f"File '{file.filename}' is too large. "
                f"Maximum allowed size: {self.max_size / (1024*1024):.2f} MB."
            )

    def _generate_unique_file_name(self, filename: str) -> str:
        return f"{uuid.uuid4()}{os.path.splitext(filename)[1]}"

    async def _save_uploaded_file(self, file: UploadFile, file_name: str):
        file_path = os.path.join(self.destination_path, file_name)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

