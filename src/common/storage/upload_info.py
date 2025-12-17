from typing import Optional, Dict


class UploadInfo:
    file_name: str
    file_size: str
    content_type: str
    metadata: Dict
    object_key: Optional[str]
    file_url: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "file_name": self.file_name,
            "file_size": self.file_size,
            "content_type": self.content_type,
            "metadata": self.metadata,
            "object_key": self.object_key,
            "file_url": self.file_url,
        }
