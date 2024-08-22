from typing import Optional, Any, List, Tuple
from .events import VkEvent, Punishment, BaseEvent
from .objects import Payload
from .objects import (
    Peer,
    User,
    Message,
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
            button (Payload, optional): Payload with data about the pressed button. If there are any.
            reaction (Payload, optional): A payload with data on the response to a message. If there are any.

        Returns:
            BaseEvent: An instance of the VkEvent class with the attributes set.
        """

        necessary_attributes = ((peer, Peer), (user, User))
        optional_attributes = (
            (message, Message),
            (button, Button),
            (reaction, Reaction),
        )

        attributes_values = cls._unpack_attr_payloads(
            necessary=necessary_attributes,
            optional=optional_attributes,
        )

        vkevent = VkEvent(type=type, event_id=id)
        for attribute in attributes_values:
            vkevent.add_object(name=attribute.__name__.lower(), value=attribute)

        return vkevent

    @classmethod
    def build_punishment(
        cls,
        type: str,
        comment: str,
        peer: Payload,
        user: Payload,
        message: Optional[Payload] = None,
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
            warn (Payload, optional): Payload with warn data. If there are any.
            unwarn (Payload, optional): Payload with unwarn data. If there are any.
            kick (Payload, optional): Payload with kick data. If there are any.

        Returns:
            BaseEvent: An instance of the Punishment class with the attributes set.
        """

        necessary_attributes = ((peer, Peer), (user, User))
        optional_attributes = (
            (message, Message),
            (warn, Warn),
            (unwarn, Unwarn),
            (kick, Kick),
        )

        attributes_values = cls._unpack_attr_payloads(
            necessary=necessary_attributes,
            optional=optional_attributes,
        )

        punishment = Punishment(type=type, comment=comment)
        for attribute in attributes_values:
            punishment.add_object(name=attribute.__name__.lower(), value=attribute)

        return punishment

    @classmethod
    @staticmethod
    def _unpack_attr_payloads(
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
