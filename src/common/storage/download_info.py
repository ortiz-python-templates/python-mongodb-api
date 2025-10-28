class DownloadInfo:
    """Represents metadata and access details of a file prepared for download."""

    def __init__(self, file_name: str, download_url: str, expires_in: int):
        """Initializes a DownloadInfo instance."""
        self.file_name = file_name
        self.download_url = download_url
        self.expires_in = expires_in

    def to_dict(self) -> dict:
        """Converts the object to a serializable dictionary representation."""
        return {
            "file_name": self.file_name,
            "download_url": self.download_url,
            "expires_in": self.expires_in
        }
