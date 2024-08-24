"""Module "database".

File:
    abc.py

About:
    File describing the Abstract Databse classe.
"""

from typing import Callable
from abc import ABC, abstractmethod
from sqlalchemy.orm import DeclarativeBase


class AbstractDB(ABC):
    @abstractmethod
    def create_tables(self, base: DeclarativeBase) -> None:
        """Creates all tables defined in the provided
        SQLAlchemy base model.

        Args:
            base (Any): The base model containing
            metadata for tables to be created.
        """
        pass

    @abstractmethod
    def drop_tables(self, base: DeclarativeBase) -> None:
        """Drops all tables defined in the provided
        SQLAlchemy base model.

        Args:
            base (Any): The base model containing
            metadata for tables to be dropped.
        """
        pass

    @abstractmethod
    def script(self, auto_commit: bool = True, debug: bool = False) -> Callable:
        """A decorator that implements a custom script wrapper.

        The decorator allows you to mark a function
        as a custom script for sqlalchemy. Using
        this mechanism, you can conveniently call
        the desired set of actions in the right place.
        """
