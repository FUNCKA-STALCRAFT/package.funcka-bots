"""Module "handler".

File:
    abc.py

About:
    File describing abstract handler class.
"""

from typing import Any
from abc import ABC, abstractmethod


class ABCHandler(ABC):
    """Abstract handler class."""

    @abstractmethod
    def __call__(self, event: Any) -> None:
        """It is necessary to implement the logic of the handler's work."""
        pass
