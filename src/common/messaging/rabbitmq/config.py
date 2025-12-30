from enum import StrEnum
from pydantic import BaseModel


class ExchangeType(StrEnum):
    FANOUT = "fanout"
    DIRECT = "direct"
    TOPIC = "topic"
    HEADERS = "headers"

class RabbitMQConfig(BaseModel):
    host: str = "localhost"
    port: int = 5672
    user: str = "guest"
    password: str = "guest"
    virtual_host: str = "/"

    def connection_string(self) -> str:
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/{self.virtual_host.lstrip('/')}"