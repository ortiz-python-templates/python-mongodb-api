from datetime import datetime, timedelta
from fastapi import UploadFile, HTTPException
from google.cloud import storage
from google.api_core import exceptions as gcs_exceptions
import uuid
from src.common.storage.upload_info import UploadInfo


class GoogleStorage:
    """Service for uploading and reading files from Google Cloud Storage (GCS)."""

    def __init__(self, bucket_name: str):
        # Initialize the Google Cloud Storage client and get the target bucket
        self._client = storage.Client()
        self.bucket_name = bucket_name
        self.bucket = self._client.bucket(bucket_name)
        

    def upload(self, file: UploadFile, bucket_prefix: str | None = None) -> UploadInfo:
        """
        Uploads a file to a private GCS bucket (with an optional folder/prefix).
        Returns an UploadInfo object containing metadata and the signed URL.
        """
        try:
            # Clean prefix and build the full blob name (unique ID + original filename)
            bucket_prefix = (bucket_prefix or "").strip("/")
            blob_name = f"{bucket_prefix}/{uuid.uuid4()}_{file.filename}" if bucket_prefix else f"{uuid.uuid4()}_{file.filename}"
            blob = self.bucket.blob(blob_name)

            # Upload the file to GCS
            blob.upload_from_file(file.file, content_type=file.content_type)

            # Try to reload the blob to fetch file size and metadata
            try:
                blob.reload()
                file_size = blob.size
            except gcs_exceptions.GoogleAPIError:
                file_size = None  # File size might be unavailable if reload fails

            # Build metadata dictionary
            metadata = {
                "blob_name": blob_name,
                "original_name": file.filename,
                "content_type": file.content_type,
                "size": file_size,
                "bucket_name": self.bucket_name,
                "uploaded_at": datetime.utcnow().isoformat() + "Z",
            }

            # Return structured upload information with a signed URL
            return UploadInfo(
                file_name=file.filename,
                file_url=self.get_file_url(blob_name),
                file_size=file_size,
                content_type=file.content_type,
                metadata=metadata,
            )

        except gcs_exceptions.Forbidden as e:
            # Handle insufficient permissions
            raise HTTPException(status_code=403, detail=f"Access denied to bucket: {e}")
        except gcs_exceptions.NotFound as e:
            # Handle missing bucket
            raise HTTPException(status_code=404, detail=f"Bucket not found: {e}")
        except Exception as e:
            # Handle any unexpected errors
            raise HTTPException(status_code=500, detail=f"File upload failed: {e}")
        finally:
            # Ensure file stream is closed after upload
            file.file.close()


    def get_file_url(self, blob_name: str, expiration_hours: int = 1) -> str:
        """
        Generates a temporary (signed) URL for accessing a private file in GCS.
        The URL expires after a configurable number of hours (default: 1 hour).
        """
        try:
            blob = self.bucket.blob(blob_name)

            # Check if the file exists before generating the signed URL
            if not blob.exists(self._client):
                raise HTTPException(status_code=404, detail="File not found in bucket")

            # Generate a signed URL for secure access
            url = blob.generate_signed_url(
                version="v4",
                expiration=timedelta(hours=expiration_hours),
                method="GET",
                response_disposition=f'inline; filename="{blob_name}"',
            )
            return url

        except gcs_exceptions.NotFound:
            raise HTTPException(status_code=404, detail="File not found")
        except gcs_exceptions.Forbidden:
            raise HTTPException(status_code=403, detail="Access denied to file")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating URL: {e}")
