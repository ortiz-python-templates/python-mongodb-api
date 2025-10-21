from datetime import datetime


class UploadInfo:
    def __init__(self, original_file_name: str, final_name: str, size: int,
                 content_type: str, extension: str, upload_time: datetime):
        self.original_file_name = original_file_name
        self.final_name = final_name
        self.size = size
        self.content_type = content_type
        self.extension = extension
        self.upload_time = upload_time