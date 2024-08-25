"""Module "broker".

File:
    publisher.py

About:
    File describing the implementation of the
    Publisher class, which facilitates publishing
    serialized objects to Redis channels.
"""

from .base import BaseWorker
from typing import Any, Optional
from loguru import logger


class Publisher(BaseWorker):
    """RabbitMQ publisher class."""

    def publish(self, obj: Any, queue_name: str) -> Optional[str]:
        """Publishes a serialized object to a queue.

        Args:
            obj (object): Object to be serialized and published.
            channel_name (str): Name of the Redis channel to publish to.

        Returns:
            int: Status code indicating the result of the publish operation.
        """
        channel = self._get_channel()
        self._check_queue(queue_name=queue_name, channel=channel)

        status = channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=self._serialize(obj),
        )
        logger.info(f"Object <{obj}> has been sent to the queue <{queue_name}>")

        return status
