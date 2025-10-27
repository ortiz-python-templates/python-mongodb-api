from datetime import datetime, timedelta
from fastapi import UploadFile, HTTPException
from google.cloud import storage
from google.api_core import exceptions as gcs_exceptions
import uuid
from src.common.storage.upload_info import UploadInfo


class GoogleStorageUploader:
    """
    Serviço para upload e leitura de arquivos no Google Cloud Storage (GCS).
    Mantém o bucket privado e gera URLs temporárias (assinadas) para acesso seguro.
    """

    def __init__(self, bucket_name: str):
        self._client = storage.Client()
        self.bucket_name = bucket_name
        self.bucket = self._client.bucket(bucket_name)

    def upload(self, file: UploadFile, bucket_prefix: str | None = None) -> UploadInfo:
        """Faz upload do arquivo para um bucket privado no GCS (com prefixo opcional)."""
        try:
            bucket_prefix = (bucket_prefix or "").strip("/")
            blob_name = f"{bucket_prefix}/{uuid.uuid4()}_{file.filename}" if bucket_prefix else f"{uuid.uuid4()}_{file.filename}"
            blob = self.bucket.blob(blob_name)

            blob.upload_from_file(file.file, content_type=file.content_type)

            try:
                blob.reload()
                file_size = blob.size
            except gcs_exceptions.GoogleAPIError:
                file_size = None

            metadata = {
                "blob_name": blob_name,
                "original_name": file.filename,
                "content_type": file.content_type,
                "size": file_size,
                "bucket_name": self.bucket_name,
                "uploaded_at": datetime.utcnow().isoformat() + "Z",
            }

            return UploadInfo(
                file_name=file.filename,
                file_url=self.get_file_url(blob_name),
                file_size=file_size,
                content_type=file.content_type,
                metadata=metadata,
            )

        except gcs_exceptions.Forbidden as e:
            raise HTTPException(status_code=403, detail=f"Acesso negado ao bucket: {e}")
        except gcs_exceptions.NotFound as e:
            raise HTTPException(status_code=404, detail=f"Bucket não encontrado: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao enviar arquivo: {e}")
        finally:
            file.file.close()


    def get_file_url(self, blob_name: str, expiration_hours: int = 1) -> str:
        """Gera uma URL temporária (assinada) para acessar o arquivo privado no GCS."""
        try:
            blob = self.bucket.blob(blob_name)
            if not blob.exists(self._client):
                raise HTTPException(status_code=404, detail="Arquivo não encontrado no bucket")

            url = blob.generate_signed_url(
                version="v4",
                expiration=timedelta(hours=expiration_hours),
                method="GET",
                response_disposition=f'inline; filename="{blob_name}"',
            )
            return url

        except gcs_exceptions.NotFound:
            raise HTTPException(status_code=404, detail="Arquivo não encontrado")
        except gcs_exceptions.Forbidden:
            raise HTTPException(status_code=403, detail="Acesso negado ao arquivo")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao gerar URL: {e}")
