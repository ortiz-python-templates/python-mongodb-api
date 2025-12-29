import gzip
import json
from typing import Any, Optional
import aio_pika
from src.common.messaging.base_producer import BaseProducer
from src.common.messaging.rabbitmq.config import ExchangeType, RabbitMQConfig


class RabbitMQProducer(BaseProducer):

    def __init__(self, config: RabbitMQConfig):
        self.config = config
        self.connection: Optional[aio_pika.RobustConnection] = None
        self.channel: Optional[aio_pika.RobustChannel] = None


    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.config.connection_string())
        self.channel = await self.connection.channel()


    async def publish(
        self, 
        topic: str, 
        key: str, 
        message: Any, 
        exchange_type: ExchangeType = ExchangeType.DIRECT
    ):
        # Declare exchange
        exchange = await self.channel.declare_exchange(
            topic, 
            type=exchange_type, 
            durable=False # matching your Go default
        )

        # Encode & Gzip (Compatibilidade com seu Go)
        body = json.dumps(message).encode("utf-8")
        compressed_body = gzip.compress(body)

        # Publish
        await exchange.publish(
            aio_pika.Message(
                body=compressed_body,
                content_type="application/json",
                content_encoding="gzip"
            ),
            routing_key=key
        )
        

    async def close(self):
        if self.connection:
            await self.connection.close()
