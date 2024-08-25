from typing import ByteString, Any
from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel
from loguru import logger
import dill as pickle


class BaseWorker:
    def __init__(self, host: str, port: int) -> None:
        params = ConnectionParameters(host=host, port=port)
        self.connection = BlockingConnection(params)

    def _get_channel(self, channel_id: int = 1) -> BlockingChannel:
        return self.connection.channel(channel_number=channel_id)

    def _check_queue(self, queue_name: str, channel: BlockingChannel) -> None:
        try:
            channel.queue_declare(queue=queue_name, passive=True)
            channel.basic_publish

        except Exception:
            channel_tag = f"Channel #{channel.channel_number}: "
            logger.warning(channel_tag + f"No queue named {queue_name} found.")

            channel.queue_declare(queue=queue_name)
            logger.info(channel_tag + f"Creating a new queue {queue_name}")

    @staticmethod
    def _serialize(obj: Any) -> ByteString:
        return pickle.dumps(obj=obj, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def _deserialize(data: ByteString) -> Any:
        return pickle.loads(str=data)
