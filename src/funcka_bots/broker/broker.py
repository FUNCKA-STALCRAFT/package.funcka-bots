"""Module "broker".

File:
    publisher.py

About:
    File describing the implementation of the
    Publisher class, which facilitates publishing
    serialized objects to Redis channels.
"""

import time
from typing import Any
from loguru import logger
from .base import BaseBroker


class Broker(BaseBroker):
    """RabbitMQ broker class."""

    def publish(self, obj: Any, queue_name: str) -> None:
        """Publishes a serialized object to a queue.

        :param Any obj: Object to be serialized and published.
        :param str queue_name: Name of the Redis channel to publish to.
        """
        channel = self._get_channel()
        self._declare_queue(queue_name=queue_name, channel=channel)

        channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=self._serialize(obj),
        )
        logger.info(f"Object <{obj}> has been sent to the queue <{queue_name}>")
        channel.close()

    def listen(self, queue_name: str, td: float = 0.2) -> Any:
        """Listens to messages on a specified RabbitMQ queue and deserializes them.

        :param str queue_name: Name of the Redis channel to listen to.
        :param float td: Delay between iterations of receiving messages. `Defaut: 0.2`.
        :return: Deserialized object received from the channel.
        :rtype: Any
        """
        channel = self._get_channel()
        self._declare_queue(queue_name=queue_name, channel=channel)

        logger.info(f"Waiting for messages from the queue '{queue_name}'...")
        while True:
            method, properties, body = channel.basic_get(
                queue=queue_name, auto_ack=True
            )
            if body is not None:
                obj = self._deserialize(body)
                logger.info(f"Received <{obj}> from the queue '{queue_name}'.")
                yield self._deserialize(body)

            else:
                time.sleep(td)

        channel.close()
