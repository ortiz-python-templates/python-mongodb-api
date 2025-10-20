import os
from dotenv import load_dotenv


if os.getenv("ENVIRONMENT") == "development":
    load_dotenv(override=True)
else:
    load_dotenv()

class EnvConfig:
    
    ENVIRONMENT = os.getenv("ENVIRONMENT")
    PORT = int(os.getenv("PORT"))

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

    # Mail
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")   
    MAIL_FROM     = os.getenv("MAIL_FROM")       
    MAIL_PORT     = int(os.getenv("MAIL_PORT", 587))
    MAIL_SERVER   = os.getenv("MAIL_SERVER")  

    # Rate Limit
    RATE_LIMIT_MAX_REQUESTS = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", 10))
    RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", 60))
     
    COOKIE_DOMAIN = os.getenv("COOKIE_DOMAIN", "localhost")

    # FILES
    UPLOADS_PATH = os.getenv("UPLOADS_PATH", "uploads")
    UPLOADS_MAX_DOCS_SIZE = int(os.getenv("UPLOADS_MAX_DOCS_SIZE", 4))  # em MB

    @classmethod
    def is_production(cls) -> bool:
        return cls.ENVIRONMENT.lower() == "production"

    @classmethod
    def is_development(cls) -> bool:
        return cls.ENVIRONMENT.lower() == "development"
    
    @classmethod
    def cookie_secure(cls) -> bool:
        return cls.is_production()
    
    @classmethod
    def app_host(cls) -> str:
        return "0.0.0.0" if cls.is_production() else "localhost"
