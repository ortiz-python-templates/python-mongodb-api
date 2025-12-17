from typing import Optional, Dict


class UploadInfo:
    file_name: str
    file_size: str
    content_type: str
    metadata: Dict
    object_key: Optional[str]
    file_url: Optional[str] = None

    def __init__(self, file_name: str, file_size: str, content_type: str, metadata: Dict, object_key: Optional[str] = None, file_url: Optional[str] = None):
        self.file_name = file_name
        self.file_size = file_size
        self.content_type = content_type
        self.metadata = metadata
        self.object_key = object_key
        self.file_url = file_url
        

    def to_dict(self) -> dict:
        return {
            "file_name": self.file_name,
            "file_size": self.file_size,
            "content_type": self.content_type,
            "metadata": self.metadata,
            "object_key": self.object_key,
            "file_url": self.file_url,
        }
