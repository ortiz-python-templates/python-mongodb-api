import json
import logging
import aio_pika
from typing import Any, Optional
from src.common.messaging.base_producer import BaseProducer
from src.common.messaging.rabbitmq.config import ExchangeType, RabbitMQConfig


class RabbitMQProducer(BaseProducer):

    def __init__(self):
        self.config = RabbitMQConfig()
        self.connection: Optional[aio_pika.RobustConnection] = None
        self.channel: Optional[aio_pika.RobustChannel] = None


    async def connect(self):
        """
        Establishes a robust connection and opens a channel.
        """
        self.connection = await aio_pika.connect_robust(self.config.connection_string())
        self.channel = await self.connection.channel()
        logging.info("RabbitMQ Producer connected successfully.")


    async def publish(
        self, 
        topic: str, 
        key: str, 
        message: Any, 
        exchange_type: ExchangeType = ExchangeType.DIRECT
    ):
        """
        Publishes a plain JSON serialized message.
        """
        if not self.channel:
            await self.connect()

        # Declare the exchange. Durable=False to match your previous default.
        exchange = await self.channel.declare_exchange(
            topic, 
            type=exchange_type, 
            durable=False
        )

        # Simple serialization: Dict -> JSON String -> Bytes
        body = json.dumps(message).encode("utf-8")

        # Publish with standard application/json metadata
        await exchange.publish(
            aio_pika.Message(
                body=body,
                content_type="application/json"
            ),
            routing_key=key
        )
        logging.info(f"Message published to Exchange '{topic}' with Routing Key '{key}'")


    async def close(self):
        """
        Gracefully closes the connection.
        """
        if self.connection:
            await self.connection.close()
            logging.info("RabbitMQ Producer connection closed.")