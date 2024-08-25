"""Module "broker".

File:
    subscriber.py

About:
    File describing the implementation of the
    Subscriber class, which listens to Redis channels
    and deserializes incoming messages.
"""

from .base import BaseWorker
from typing import Any
from loguru import logger


class Subscriber(BaseWorker):
    """RabbitMQ subscriber class."""

    def listen(self, queue_name: str) -> Any:
        """Listens to messages on a specified RabbitMQ queue and deserializes them.

        :param st channel_name: Name of the Redis channel to listen to.
        :return: Deserialized object received from the channel.
        :rtype: Any
        """
        channel = self._get_channel()
        self._check_queue(queue_name=queue_name, channel=channel)

        logger.info(f"Waiting for messages from the queue '{queue_name}'...")
        while True:
            method, properties, body = channel.basic_get(
                queue=queue_name, auto_ack=True
            )
            if body is not None:
                obj = self._deserialize(body)
                logger.info(f"Received <{obj}> from the queue '{queue_name}'.")
                yield self._deserialize(body)
