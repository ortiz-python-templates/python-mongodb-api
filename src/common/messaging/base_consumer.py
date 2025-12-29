from abc import ABC, abstractmethod
from typing import Any, Awaitable, Callable


class BaseConsumer(ABC):
    
    @abstractmethod
    async def subscribe(self, topic: str, key: str, handler: Callable[[Any], Awaitable[None]]) -> None:
        """Subscribes to a topic and executes a handler for each received message."""
        pass

    @abstractmethod
    async def listen_and_log(self, topic: str, key: str) -> None:
        """Listens to a topic and logs messages to the console for debugging purposes."""
        pass