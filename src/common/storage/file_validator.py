import os
from fastapi import UploadFile, HTTPException, status


class FileValidator:
    def __init__(self, allowed_extensions: list[str], max_size_mb: int):
        self.allowed_extensions = [ext.lower() for ext in allowed_extensions]
        self.max_size = max_size_mb * 1024 * 1024  # bytes

    def validate(self, file: UploadFile):
        # Validar extensão
        _, file_ext = os.path.splitext(file.filename)
        file_ext = file_ext.lower()

        if file_ext not in self.allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Extensão '{file_ext}' não permitida. Permitidas: {', '.join(self.allowed_extensions)}",
            )

        # Validar tamanho
        file.file.seek(0, os.SEEK_END)
        size = file.file.tell()
        file.file.seek(0)

        if size > self.max_size:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"O ficheiro '{file.filename}' excede o limite de {self.max_size / (1024*1024):.1f} MB",
            )
