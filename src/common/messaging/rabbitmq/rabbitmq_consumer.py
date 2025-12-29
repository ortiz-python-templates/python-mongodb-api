import logging
import aio_pika
import gzip
import json
from typing import Any, Callable, Awaitable
from src.common.messaging.base_consumer import BaseConsumer
from src.common.messaging.rabbitmq.config import RabbitMQConfig


class RabbitMQConsumer(BaseConsumer):

    def __init__(self, config: RabbitMQConfig):
        self.config = config
        self.connection = None
        self.channel = None


    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.config.connection_string())
        self.channel = await self.connection.channel()


    async def subscribe(
        self, 
        exchange_name: str, 
        routing_key: str, 
        callback: Callable[[Any], Awaitable[None]]
    ):
        # Declare exchange
        exchange = await self.channel.declare_exchange(exchange_name, type="direct")
        
        # Declare temporary queue (Go default: exclusive=True)
        queue = await self.channel.declare_queue("", exclusive=True)
        await queue.bind(exchange, routing_key=routing_key)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    # Decompress & Decode
                    decompressed = gzip.decompress(message.body)
                    data = json.loads(decompressed)
                    
                    # Execute provided function
                    await callback(data)


    async def listen_and_log(self, topic: str, key: str) -> None:
        """Listens to a topic and logs messages (Equivalent to ConsumeFromExchange/logMessages in Go)."""
        
        async def logger_handler(data: Any) -> None:
            # Equivalent to log.Printf("Received a message: %s", msg.Body)
            logging.info(f"Received a message: {json.dumps(data, indent=2)}")

        # Reuses subscribe logic with the logger handler
        await self.subscribe(topic, key, logger_handler)