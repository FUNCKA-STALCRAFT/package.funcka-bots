from funcka_bots.events import BaseEvent
from funcka_bots.broker import (
    Subscriber,
    Publisher,
    build_connection,
)
from .credentials import RedisCredentials


publisher = Publisher(client=build_connection(creds=RedisCredentials))
subscriber = Subscriber(client=build_connection(creds=RedisCredentials))


def listen() -> None:
    for event in subscriber.listen(channel_name="my_channel"):
        print(f"Получено новое событие: {event}")

        # Some actions with event


def public(event: BaseEvent) -> None:
    publisher.publish(obj=event, channel_name="other_channel")


# The broker shell implemented over Redis is able to
# accept objects, serialize and send them to
# one of the Redis databases. Therefore, I'm importing the library
# # funka_bots in 2 different services, they will send each other
# # other objects that can be used in the future
# code. Their functionality and all their attributes are fully preserved.
