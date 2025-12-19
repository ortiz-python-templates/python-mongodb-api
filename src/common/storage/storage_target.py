from enum import StrEnum


class StorageProvider(StrEnum):
    FILESYSTEM = "filesystem"
    MINIO = "minio"
    GCS = "gcs"
    AWS_S3 = "aws-s3"
    AZURE_BLOB = "azure-blob"
