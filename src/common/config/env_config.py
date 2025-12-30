import os
from dotenv import load_dotenv


if os.getenv("APP_ENVIRONMENT") == "development":
    load_dotenv(override=True)
else:
    load_dotenv()

class EnvConfig:
    
    APP_ENVIRONMENT = os.getenv("APP_ENVIRONMENT", "development")
    APP_NAME = os.getenv("APP_NAME", "python-template-mongodb-api")
    APP_PORT = int(os.getenv("APP_PORT", 5000))
    APP_VERSION = os.getenv("APP_VERSION")

    # Mongo
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DATABASE = os.getenv("MONGO_DATABASE")

    # Redis
    REDIS_URL = os.getenv("REDIS_URL")

    # JWT
    JWT_SECRET_KEY  = os.getenv("JWT_SECRET_KEY")
    JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 15))
    JWT_REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_DAYS", 7))
    JWT_COOKIE_DOMAIN  = os.getenv("JWT_COOKIE_DOMAIN")
    JWT_COOKIE_SAME_SITE = os.getenv("JWT_COOKIE_SAME_SITE", "Lax")
    JWT_COOKIE_ACCESS_NAME = os.getenv("JWT_COOKIE_ACCESS_NAME", "access_token")
    JWT_COOKIE_REFRESH_NAME = os.getenv("JWT_COOKIE_REFRESH_NAME", "refresh_token")

    # Mail
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")   
    MAIL_FROM     = os.getenv("MAIL_FROM")       
    MAIL_PORT     = int(os.getenv("MAIL_PORT", 587))
    MAIL_SERVER   = os.getenv("MAIL_SERVER")  

    # Rate Limit
    RATE_LIMIT_MAX_REQUESTS = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", 10))
    RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", 60))

    # Messaging (RabbitMQ)
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
    RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
    RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
    RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")
    RABBITMQ_VIRTUAL_HOST = os.getenv("RABBITMQ_VIRTUAL_HOST", "/")

    # Outbox Worker
    OUTBOX_POLLING_INTERVAL_SECONDS = int(os.getenv("OUTBOX_POLLING_INTERVAL_SECONDS", 5))
    OUTBOX_BATCH_SIZE = int(os.getenv("OUTBOX_BATCH_SIZE", 100))
    OUTBOX_MAX_RETRIES = int(os.getenv("OUTBOX_MAX_RETRIES", 5))
     
    # File max sizes
    MAX_DOCUMENT_FILE_SIZE_MB = int(os.getenv("MAX_DOCUMENT_FILE_SIZE_MB", 5))
    MAX_IMAGE_FILE_SIZE_MB = int(os.getenv("MAX_IMAGE_FILE_SIZE_MB", 5))
    MAX_ARCHIVE_FILE_SIZE_MB = int(os.getenv("MAX_ARCHIVE_FILE_SIZE_MB", 10))

    STORAGE_PROVIDER = os.getenv("STORAGE_PROVIDER", "minio") # values: minio | gcs | filesystem

    # File system uploads
    FILESYSTEM_STORAGE_PATH = os.getenv("FILESYSTEM_STORAGE_PATH", "/var/lib/python-mongodb-api/uploads")

    # MinIO configuration
    MINIO_ROOT_USER = os.getenv("MINIO_ROOT_USER","admin")
    MINIO_ROOT_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD", "admin123")
    MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://localhost:9000")
    MINIO_MAIN_BUCKET = os.getenv("MINIO_MAIN_BUCKET", "python-mongodb-bucket")

    # Google 
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    GOOGLE_STORAGE_MAIN_BUCKET = os.getenv("GOOGLE_STORAGE_MAIN_BUCKET", "python-mongodb-bucket")

    @classmethod
    def is_production(cls) -> bool:
        return cls.APP_ENVIRONMENT.lower() == "production"

    @classmethod
    def is_development(cls) -> bool:
        return cls.APP_ENVIRONMENT.lower() == "development"
    
    @classmethod
    def cookie_secure(cls) -> bool:
        return cls.is_production()
    
    @classmethod
    def minio_secure(cls) -> bool:
        return cls.is_production()
    
    @classmethod
    def app_host(cls) -> str:
        return "0.0.0.0" if cls.is_production() else "localhost"
