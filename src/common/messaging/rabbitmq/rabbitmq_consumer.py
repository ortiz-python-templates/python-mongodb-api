import aio_pika
import gzip
import json
from typing import Any, Callable, Awaitable
from src.common.messaging.rabbitmq.config import RabbitMQConfig


class RabbitMQConsumer:
    def __init__(self, config: RabbitMQConfig):
        self.config = config
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.config.connection_string())
        self.channel = await self.connection.channel()

    async def process_message_from_exchange(
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