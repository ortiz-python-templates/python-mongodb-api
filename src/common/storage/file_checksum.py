import hashlib
import base64
from typing import Union, IO


class FileChecksum:
    """Utility class to calculate and verify file checksums using various algorithms."""

    @staticmethod
    def calculate_checksum(file_bytes: bytes, algorithm: str = "sha256") -> str:
        """
        Calculate the checksum of a byte array.
        """
        h = hashlib.new(algorithm)
        h.update(file_bytes)
        return h.hexdigest()


    @staticmethod
    def calculate_checksum_stream(file_obj: IO[bytes], chunk_size: int = 8192, algorithm: str = "sha256") -> str:
        """
        Calculate the checksum of a file-like object incrementally (for large files).
        """
        h = hashlib.new(algorithm)
        while chunk := file_obj.read(chunk_size):
            h.update(chunk)
        return h.hexdigest()


    @staticmethod
    def verify_checksum(file_bytes: Union[bytes, IO[bytes]], expected_checksum: str, algorithm: str = "sha256") -> bool:
        """
        Verify that the file's checksum matches the expected checksum.
        """
        if isinstance(file_bytes, bytes):
            actual_checksum = FileChecksum.calculate_checksum(file_bytes, algorithm)
        else:
            actual_checksum = FileChecksum.calculate_checksum_stream(file_bytes, algorithm=algorithm)

        return actual_checksum == expected_checksum


    @staticmethod
    def calculate_checksum_b64(file_bytes: bytes, algorithm: str = "sha256") -> str:
        """
        Calculate the checksum and return it as a Base64-encoded string.
        """
        h = hashlib.new(algorithm)
        h.update(file_bytes)
        return base64.b64encode(h.digest()).decode()
