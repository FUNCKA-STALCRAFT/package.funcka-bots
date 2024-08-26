"""Module "broker".

File:
    publisher.py

About:
    File describing the implementation of the
    Publisher class, which facilitates publishing
    serialized objects to Redis channels.
"""

from .base import BaseWorker
from typing import Any
from loguru import logger


class Publisher(BaseWorker):
    """RabbitMQ publisher class."""

    def publish(self, obj: Any, queue_name: str) -> None:
        """Publishes a serialized object to a queue.

        :param Any obj: Object to be serialized and published.
        :param str queue_name: Name of the Redis channel to publish to.
        """
        self._pre_ping()

        channel = self._get_channel()
        self._declare_queue(queue_name=queue_name, channel=channel)

        channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=self._serialize(obj),
        )
        logger.info(f"Object <{obj}> has been sent to the queue <{queue_name}>")
        channel.close()
