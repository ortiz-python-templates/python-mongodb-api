import uuid
from datetime import timedelta
from minio import Minio
from fastapi import UploadFile
from src.common.storage.units_of_measurement import UnitsOfMeasurement


class MinioStorage:
    """
    Service for uploading and retrieving files from a MinIO object storage.
    Automatically creates the target bucket if it does not exist.
    """

    def __init__(self, endpoint, access_key, secret_key, bucket_name):
        # Initialize MinIO client (secure=False means HTTP; set True for HTTPS)
        self.client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=False)
        self.bucket_name = bucket_name

        # Ensure the bucket exists, create it if necessary
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)


    def upload(self, file: UploadFile) -> str:
        """Uploads a file to MinIO and returns a temporary signed URL."""
        # Generate a unique name to avoid overwriting files
        object_name = f"{uuid.uuid4()}_{file.filename}"

        # Upload file stream to MinIO bucket
        self.client.put_object(
            self.bucket_name,
            object_name,
            file.file,
            length=-1,  # Allows streaming uploads of unknown length
            part_size=10 * UnitsOfMeasurement.MEGA_BYTE  # Split large uploads into 10 MB parts
        )

        # Generate a signed URL that expires in 1 hour (3600 seconds)
        url = self.client.presigned_get_object(
            self.bucket_name, object_name, 
            expires=timedelta(seconds=3600)
        )
        return url


    def get_file_url(self, object_name: str, expires_in_seconds: int = 3600) -> str:
        """Generates a signed URL for an existing object in the MinIO bucket."""
        return self.client.presigned_get_object(self.bucket_name, object_name, expires=expires_in_seconds)
