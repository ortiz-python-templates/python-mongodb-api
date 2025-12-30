from enum import StrEnum
from pydantic import BaseModel
from src.common.config.env_config import EnvConfig


class ExchangeType(StrEnum):
    FANOUT = "fanout"
    DIRECT = "direct"
    TOPIC = "topic"
    HEADERS = "headers"

class RabbitMQConfig(BaseModel):
    host: str = EnvConfig.RABBITMQ_HOST
    port: int = EnvConfig.RABBITMQ_PORT
    user: str = EnvConfig.RABBITMQ_USER
    password: str = EnvConfig.RABBITMQ_PASSWORD
    virtual_host: str = EnvConfig.RABBITMQ_VIRTUAL_HOST

    def connection_string(self) -> str:
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/{self.virtual_host.lstrip('/')}"