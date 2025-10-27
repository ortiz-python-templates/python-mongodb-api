import uuid
from minio import Minio
from fastapi import UploadFile


class MinioStorage:

    def __init__(self, endpoint, access_key, secret_key, bucket_name):
        self.client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=False)
        self.bucket_name = bucket_name
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)

    def upload(self, file: UploadFile) -> str:
        object_name = f"{uuid.uuid4()}_{file.filename}"
        self.client.put_object(
            self.bucket_name,
            object_name,
            file.file,
            length=-1,  # permite streaming
            part_size=10*1024*1024  # 10 MB
        )
        # Retorna URL temporária (signed URL)
        url = self.client.presigned_get_object(self.bucket_name, object_name, expires=3600)
        return url

    def get_file_url(self):
        pass