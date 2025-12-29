from abc import ABC, abstractmethod
from typing import Any


class BaseProducer(ABC):
    
    @abstractmethod
    async def connect(self) -> None:
        """Establishes a connection with the message broker."""
        pass

    @abstractmethod
    async def publish(self, topic: str, key: str, message: Any) -> None:
        """Publishes a message to a specific topic using a routing key."""
        pass

    @abstractmethod
    async def close(self) -> None:
        """Closes the connection to the message broker safely."""
        pass