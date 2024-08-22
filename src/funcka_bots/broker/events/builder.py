from typing import Optional, Any, List, Tuple
from .events import VkEvent, Punishment, BaseEvent
from .objects import Payload
from .objects import (
    Peer,
    User,
    Message,
    Reply,
    Reaction,
    Button,
    Kick,
    Warn,
    Unwarn,
)

ValStructPair = Tuple[Tuple[Payload, Any]]
AttrValues = List[Any]


class EventBuilder:
    """Event builder.

    Description:
        It offers an interface for convenient and centralized
        event construction. It does not require class initialization.
    """

    @classmethod
    def build_vkevent(
        cls,
        type: str,
        id: int,
        peer: Payload,
        user: Payload,
        message: Optional[Payload] = None,
        message_reply: Optional[Payload] = None,
        message_forward: Optional[List[Payload]] = None,
        button: Optional[Payload] = None,
        reaction: Optional[Payload] = None,
    ) -> BaseEvent:
        """Creates and returns an instance of the VkEvent class.

        Args:
            type (str): The type of the event.
            id (int): The event ID.
            peer (Payload): Payload with conversation data.
            user (Payload): Payload with user data.
            message (Payload, optional): Payload with message data. If there are any.
            message_reply
            message_forward
            button (Payload, optional): Payload with data about the pressed button. If there are any.
            reaction (Payload, optional): A payload with data on the response to a message. If there are any.

        Returns:
            BaseEvent: An instance of the VkEvent class with the attributes set.
        """

        cls._cat_message_payloads(message, message_reply, message_forward)

        necessary_attributes = ((peer, Peer), (user, User))
        optional_attributes = (
            (message, Message),
            (button, Button),
            (reaction, Reaction),
        )

        vkevent = cls._build_event(
            class_=VkEvent,
            necessary_attributes=necessary_attributes,
            optional_attributes=optional_attributes,
        )
        return vkevent

    @classmethod
    def build_punishment(
        cls,
        type: str,
        comment: str,
        peer: Payload,
        user: Payload,
        message: Optional[Payload] = None,
        message_reply: Optional[Payload] = None,
        message_forward: Optional[List[Payload]] = None,
        warn: Optional[Payload] = None,
        unwarn: Optional[Payload] = None,
        kick: Optional[Payload] = None,
    ) -> BaseEvent:
        """Creates and returns an instance of the Punishment class.

        Args:
            type (str): The type of the event.
            id (int): The event ID.
            peer (Payload): Payload with conversation data.
            user (Payload): Payload with user data.
            message (Payload, optional): Payload with message data. If there are any.
            message_reply
            message_forward
            warn (Payload, optional): Payload with warn data. If there are any.
            unwarn (Payload, optional): Payload with unwarn data. If there are any.
            kick (Payload, optional): Payload with kick data. If there are any.

        Returns:
            BaseEvent: An instance of the Punishment class with the attributes set.
        """
        cls._cat_message_payloads(message, message_reply, message_forward)

        necessary_attributes = ((peer, Peer), (user, User))
        optional_attributes = (
            (message, Message),
            (warn, Warn),
            (unwarn, Unwarn),
            (kick, Kick),
        )

        punishment = cls._build_event(
            class_=Punishment,
            necessary_attributes=necessary_attributes,
            optional_attributes=optional_attributes,
        )
        return punishment

    @classmethod
    def _build_event(
        cls,
        class_: Any,
        necessary_attributes: ValStructPair = (),
        optional_attributes: ValStructPair = (),
    ):
        attributes_values = cls._unpack_attributes_payloads(
            necessary=necessary_attributes,
            optional=optional_attributes,
        )

        event = class_(type=type, event_id=id)
        cls._set_event_attributes(attributes_values, event)

        return event

    @classmethod
    @staticmethod
    def _cat_message_payloads(message, reply, forward) -> None:
        if message:
            message["reply"] = reply if reply is None else Reply(**reply)
            message["forward"] = (
                [] if forward is None else [Reply(**fwd) for fwd in forward]
            )

    @classmethod
    @staticmethod
    def _unpack_attributes_payloads(
        necessary: ValStructPair,
        optional: ValStructPair,
    ) -> AttrValues:
        attr_values = []

        for attr, struct in necessary:
            attr_values.append(struct(**attr))

        for attr, struct in optional:
            if attr is not None:
                attr_values.append(struct(**attr))

        return attr_values

    @classmethod
    @staticmethod
    def _set_event_attributes(attributes_values: AttrValues, event: BaseEvent) -> None:
        for attribute in attributes_values:
            event.add_object(name=attribute.__name__.lower(), value=attribute)
