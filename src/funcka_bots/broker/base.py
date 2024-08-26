from typing import ByteString, Any, Optional
from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel
from pika.credentials import PlainCredentials
from pika.exceptions import AMQPConnectionError
from funcka_bots.credentials import RabbitMQCredentials
from loguru import logger
import dill as pickle


class BaseWorker:
    def __init__(self, creds: RabbitMQCredentials) -> None:
        self.params = ConnectionParameters(
            host=creds.host,
            port=creds.port,
            virtual_host=creds.vhost,
            credentials=PlainCredentials(
                username=creds.user,
                password=creds.pswd,
            ),
            heartbeat=120,
            blocked_connection_timeout=100,
        )
        self._connect()

    def _connect(self, attempts: int = 5) -> None:
        try:
            attempts -= 1
            self.connection = BlockingConnection(self.params)

        except AMQPConnectionError as e:
            logger.info(f"Error connecting to RabbitMQ: {e}")
            if attempts > 0:
                logger.info("Reconnecting... ")
                self._connect(attempts)

            else:
                logger.error("Failed to connect to RabbitMQ.")

    def _pre_ping(self):
        if not (self.connection and self.connection.is_open):
            self.connect()

    def _get_channel(self, channel_id: Optional[int] = None) -> BlockingChannel:
        return self.connection.channel(channel_number=channel_id)

    def _declare_queue(self, queue_name: str, channel: BlockingChannel) -> None:
        channel.queue_declare(queue=queue_name, durable=True)

    @staticmethod
    def _serialize(obj: Any) -> ByteString:
        return pickle.dumps(obj=obj, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def _deserialize(data: ByteString) -> Any:
        return pickle.loads(str=data)
