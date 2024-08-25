from typing import ByteString, Any, Optional
from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel
from pika.credentials import PlainCredentials
from funcka_bots.credentials import RabbitMQCredentials
from loguru import logger
import dill as pickle


class BaseWorker:
    def __init__(self, creds: RabbitMQCredentials) -> None:
        params = ConnectionParameters(
            host=creds.host,
            port=creds.port,
            virtual_host=creds.vhost,
            credentials=PlainCredentials(
                username=creds.user,
                password=creds.pswd,
            ),
        )
        self.connection = BlockingConnection(params)

    def _get_channel(self, channel_id: Optional[int] = None) -> BlockingChannel:
        return self.connection.channel(channel_number=channel_id)

    def _check_queue(self, queue_name: str, channel: BlockingChannel) -> None:
        try:
            channel.queue_declare(queue=queue_name, passive=True)

        except Exception:
            channel_tag = f"Channel #{channel.channel_number}: "
            logger.warning(channel_tag + f"No queue named '{queue_name}' found.")

            channel.queue_declare(queue=queue_name)
            logger.info(channel_tag + f"Creating a new queue '{queue_name}'.")

    @staticmethod
    def _serialize(obj: Any) -> ByteString:
        return pickle.dumps(obj=obj, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def _deserialize(data: ByteString) -> Any:
        return pickle.loads(str=data)
