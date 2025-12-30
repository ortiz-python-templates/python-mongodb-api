import logging
import aio_pika
import json
from typing import Any, Callable, Awaitable, Optional
from src.common.messaging.base_consumer import BaseConsumer
from src.common.messaging.rabbitmq.config import RabbitMQConfig

class RabbitMQConsumer(BaseConsumer):

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
        logging.info("RabbitMQ Consumer connected successfully.")


    async def subscribe(
        self, 
        exchange_name: str, 
        routing_key: str, 
        callback: Callable[[Any], Awaitable[None]]
    ):
        """
        Subscribes to an exchange using a temporary exclusive queue.
        """
        if not self.channel:
            await self.connect()

        # Declare exchange
        exchange = await self.channel.declare_exchange(exchange_name, type="direct")
        
        # Declare temporary queue (exclusive=True ensures it is deleted on disconnect)
        queue = await self.channel.declare_queue("", exclusive=True)
        await queue.bind(exchange, routing_key=routing_key)

        logging.info(f"Subscribed to exchange '{exchange_name}' with routing key '{routing_key}'")

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    try:
                        # Direct JSON decoding from bytes
                        data = json.loads(message.body.decode("utf-8"))
                        
                        # Execute the provided callback function
                        await callback(data)
                    except json.JSONDecodeError as e:
                        logging.error(f"Failed to decode JSON message: {e}")
                    except Exception as e:
                        logging.error(f"Error processing message: {e}")


    async def listen_and_log(self, topic: str, key: str) -> None:
        """
        Listens to a topic and logs messages.
        """
        async def logger_handler(data: Any) -> None:
            logging.info(f"Received message: {json.dumps(data, indent=2)}")

        # Reuse subscribe logic with the logger handler
        await self.subscribe(topic, key, logger_handler)


    async def close(self):
        """
        Gracefully closes the connection.
        """
        if self.connection:
            await self.connection.close()
            logging.info("RabbitMQ Consumer connection closed.")