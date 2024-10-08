"""Module "events".

File:
    objects.py

About:
    File describing implementation of various
    NamedTuple classes used for representing different
    types of event objects.
"""

from __future__ import annotations
from typing import NamedTuple, List, Optional, Dict, Union


Payload = Dict[str, Union[str, int]]


class Button(NamedTuple):
    """Class for representing a button press.

    Arguments:
        cmid (int): Conversation message ID.
        beid (str): Button event (press) ID.
        payload (Payload): Button payload.
    """

    cmid: int
    beid: str
    payload: Payload


class Message(NamedTuple):
    """Class for representing a message.

    Arguments:
        cmid (int): Conversation message ID.
        text (str): Message text.
        reply (Optional[Reply]): Replied message.
        forward (List[Reply]): Forwarded messages.
        attachments (List[str]): Message attachments.
    """

    cmid: int
    text: str
    reply: Optional[Reply]
    forward: List[Reply]
    attachments: List[str]


class Reaction(NamedTuple):
    """Class for representing a reaction to a message.

    Arguments:
        cmid (int): Conversation message ID.
        rid (int): Reaction ID.
    """

    cmid: int
    rid: int


class Reply(NamedTuple):
    """Class for representing a reply(fwd) to a message.

    Arguments:
        uuid (int): User unique ID. Replied message owner.
        cmid (int): Conversation message ID.
        text (str): Message text.
    """

    uuid: int
    cmid: int
    text: str


class User(NamedTuple):
    """Class for representing a user.

    Arguments:
        uuid (int): User unique ID.
        name (str): Full user name.
        firstname (str): First name.
        lastname (str): Last name.
        nick (str): Tag/nick/URL.
    """

    uuid: int
    name: str
    firstname: str
    lastname: str
    nick: str


class Peer(NamedTuple):
    """Class for representing a peer.

    Arguments:
        bpid (int): Bot peer ID.
        cid (int): Chat ID.
        name (str): Peer name.
    """

    bpid: int
    cid: int
    name: str


class Warn(NamedTuple):
    """Class for representing a Warn punishment.

    Arguments:
        points (int): The number of warn points.
    """

    points: int


class Unwarn(Warn):
    """The same as Warn.
    Implies a negative number of points.
    """


class Kick(NamedTuple):
    """Class for representing a Kick punishment.

    Arguments:
        mode (str): Kick mode.
    """

    mode: str
