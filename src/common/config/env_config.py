import os
from dotenv import load_dotenv


if os.getenv("APP_ENVIRONMENT") == "development":
    load_dotenv(override=True)
else:
    load_dotenv()

class EnvConfig:
    
    APP_ENVIRONMENT = os.getenv("APP_ENVIRONMENT", "development")
    APP_NAME=os.getenv("APP_NAME", "python-template-mongodb-api")
    APP_PORT = int(os.getenv("APP_PORT", 5000))

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

    # Mail
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")   
    MAIL_FROM     = os.getenv("MAIL_FROM")       
    MAIL_PORT     = int(os.getenv("MAIL_PORT", 587))
    MAIL_SERVER   = os.getenv("MAIL_SERVER")  

    # Rate Limit
    RATE_LIMIT_MAX_REQUESTS = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", 10))
    RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", 60))
     
   # File max sizes
    MAX_DOCUMENT_FILE_SIZE_MB = int(os.getenv("MAX_DOCUMENT_FILE_SIZE_MB", 5))
    MAX_IMAGE_FILE_SIZE_MB = int(os.getenv("MAX_IMAGE_FILE_SIZE_MB", 5))
    MAX_ARCHIVE_FILE_SIZE_MB = int(os.getenv("MAX_ARCHIVE_FILE_SIZE_MB", 10))

    # File system uploads
    FILE_SYSTEM_UPLOAD_PATH=os.getenv("FILE_SYSTEM_UPLOAD_PATH", "/var/www/uploads")

    # MinIO configuration
    MINIO_ROOT_USER = os.getenv("MINIO_ROOT_USER","admin")
    MINIO_ROOT_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD", "admin123")
    MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    MINIO_MAIN_BUCKET = os.getenv("MINIO_MAIN_BUCKET", "python-mongodb-bucket")

    # Google 
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    GOOGLE_STORAGE_MAIN_BUCKET = os.getenv("GOOGLE_STORAGE_MAIN_BUCKET")

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
    def app_host(cls) -> str:
        return "0.0.0.0" if cls.is_production() else "localhost"
