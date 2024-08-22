"""Module "events".

File:
    events.py

About:
    File describing custom Event class.
"""

from typing import Dict, Union, Any
from abc import ABC, abstractmethod


Payload = Dict[str, Union[str, int]]


class ABCEvent(ABC):
    @abstractmethod
    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        return self.__str__()

    def as_dict(self) -> Payload:
        """Converts the ABCEvent object to a dictionary.

        Description:
            This method is used only for logging
            purposes and is not intended for future
            data exchange.

        Returns:
            dict: Dictionary representation.
        """

        dict_repr = {}
        for attr, value in vars(self).items():
            if not callable(value) and not attr.startswith("__"):
                if isinstance(value, tuple):
                    dict_repr[attr] = value._asdict()
                else:
                    dict_repr[attr] = value

        return dict_repr


class BaseEvent(ABCEvent):
    """The base event.

    Description:
        It includes an empty shell with no hint of
        data storage. It is necessary, first of all, for
        typhining. It is from him that events are inherited
        VkEvent, Punishment, etc.
    """

    def __str__(self) -> str:
        return "<The basic event of the bot.>"

    def add_object(self, name: str, value: Any) -> None:
        """Adds the event data object as an attribute
        of the class.

        Args:
            name (str): Object name.
            value (Any): Object value.
        """

        self.__setattr__(name, value)


class VkEvent(ABCEvent):
    """Class for representing an vk event.

    Attributes:
        event_id (str): Unique identifier for the event.
        event_type (str): Type of the event.

    ---OPTIONAL---
    Dynamically defined attributes:
        Always determined:
            user (User): Data of the user who called the event.
            peer (Peer): Data of the peer where the event occurred.

        Determined depending on the type of event:
            button (Button): Button click data.
            reaction (Reaction): Reaction data for the message.
            message (Message): Message data.
    """

    event_id: str = None
    event_type: str = None

    def __init__(self, event_id: str, type: str):
        self.event_type = type
        self.event_id = event_id

    def __str__(self) -> str:
        string = (
            "<-- "
            f"class Event <type: {self.event_type}>"
            " | "
            f"<id: {self.event_id}>"
            " -->"
        )
        return string


class Punishment(ABCEvent):
    """Class for representing an punishment.

    Attributes:
        punishment_type (str): Type of the punishment.
        comment (str): Comment for punishment.

    ---OPTIONAL---
    Dynamically defined attributes:
        Always determined:
            user (User): Data of the user who called the event.
            peer (Peer): Data of the peer where the event occurred.

        Determined depending on the context of punishment:
            message (Message): Message data.
            warn (Warn): The data required to issue a warning.
            unwarn: The data required to remove the warning.
            kick (Kick): The data required to exclude the user.

    """

    punishment_type: str = None
    comment: str = None

    def __init__(self, type: str, comment: str) -> None:
        self.punishment_type = type
        self.comment = comment

    def __str__(self) -> str:
        string = (
            "<-- "
            f"class Punishment <type: {self.punishment_type}>"
            " | "
            f"<comment: {self.comment}>"
            " -->"
        )
        return string
