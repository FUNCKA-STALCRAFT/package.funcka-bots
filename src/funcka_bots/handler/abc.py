"""Module "handler".

File:
    abc.py

About:
    File describing abstract handler class.
"""

from funcka_bots.events import BaseEvent
from abc import ABC, abstractmethod


class ABCHandler(ABC):
    """Abstract handler class."""

    @abstractmethod
    def __call__(self, event: BaseEvent) -> None:
        """It is necessary to implement the logic of the handler's work."""
        pass
