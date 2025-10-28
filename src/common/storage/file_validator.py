import os
from fastapi import UploadFile, HTTPException, status
from src.common.storage.units_of_measurement import UnitsOfMeasurement


class FileValidator:
    """Validates uploaded files by checking their extension and size against allowed rules."""

    def __init__(self, allowed_extensions: list[str], max_size: int, unit: int = UnitsOfMeasurement.MEGA_BYTE):
        """
        :param allowed_extensions: Allowed file extensions (e.g. [".jpg", ".pdf"])
        :param max_size: Maximum allowed size (numeric value)
        :param unit: Unit of measurement from UnitsOfMeasurement (default: MB)
        """
        self.allowed_extensions = [ext.lower() for ext in allowed_extensions]
        self.max_size_bytes = max_size * unit
        self.max_size = max_size
        self.unit = unit

    def validate(self, file: UploadFile):
        # Validate extension
        _, file_ext = os.path.splitext(file.filename)
        file_ext = file_ext.lower()

        if file_ext not in self.allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Extension '{file_ext}' not allowed. Allowed: {', '.join(self.allowed_extensions)}",
            )

        # Validate size
        file.file.seek(0, os.SEEK_END)
        size = file.file.tell()
        file.file.seek(0)

        if size > self.max_size_bytes:
            unit_name = self._get_unit_name()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The file '{file.filename}' exceeds the limit of {self.max_size} {unit_name}.",
            )
        
    
        def _get_unit_name(self):
            """Returns a readable name for the unit"""
            mapping = {
                UnitsOfMeasurement.BYTE: "Bytes",
                UnitsOfMeasurement.KILO_BYTE: "KB",
                UnitsOfMeasurement.MEGA_BYTE: "MB",
                UnitsOfMeasurement.GIGA_BYTE: "GB",
                UnitsOfMeasurement.TERA_BYTE: "TB",
            }
            return mapping.get(self.unit, "Bytes")

