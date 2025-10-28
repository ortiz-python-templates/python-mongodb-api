class UploadInfo:
    """Represents metadata and access details of a file uploaded to storage."""

    def __init__(self, file_name: str, file_url: str, file_size: str, content_type: str, metadata: dict):
        self.file_name = file_name
        self.file_url = file_url
        self.file_size = file_size
        self.content_type = content_type
        self.metadata = metadata

    def to_dict(self):
        return {
            "file_name": self.file_name,
            "file_url": self.file_url,
            "file_size": self.file_size,
            "content_type": self.content_type,
            "metadata": self.metadata
        }
