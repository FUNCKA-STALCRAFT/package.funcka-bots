from typing import Callable, Any, Union
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy import Engine
from loguru import logger
from .abc import AbstractDB


class BaseDB(AbstractDB):
    def __init__(
        self,
        engine_creation_func: Callable,
        session_class: Any,
        connection_uri: str,
        debug: bool,
    ) -> None:
        self._engine = engine_creation_func(
            connection_uri, echo=debug, pool_pre_ping=True
        )
        self._session = sessionmaker(
            bind=self._engine, autoflush=False, class_=session_class
        )

    def make_session(self) -> Union[Session, AsyncSession]:
        """Creates and returns a new SQLAlchemy session.

        Returns:
            Session: A new SQLAlchemy session.
        """
        return self._session()

    def get_engine(self) -> Union[Engine, AsyncEngine]:
        """Returns the SQLAlchemy engine instance.

        Returns:
            Engine: The SQLAlchemy engine instance.
        """
        return self._engine

    def _handle_script_exception(error: Exception, func: Callable) -> None:
        text = (
            f"Script <{func.__name__}> execution failed. "
            "Transaction rolled back. \n"
            f"ErrorMessage: {error}"
        )
        logger.error(text)

    def create_tables(self, base: DeclarativeBase) -> None:
        """Creates all tables defined in the provided
        SQLAlchemy base model.

        Args:
            base (Any): The base model containing
            metadata for tables to be created.
        """
        raise NotImplementedError("This method should be redefined in the subclass")

    def drop_tables(self, base: DeclarativeBase) -> None:
        """Drops all tables defined in the provided
        SQLAlchemy base model.

        Args:
            base (Any): The base model containing
            metadata for tables to be dropped.
        """
        raise NotImplementedError("This method should be redefined in the subclass")

    def script(self, auto_commit: bool = True, debug: bool = False) -> Callable:
        """A decorator that implements a custom script wrapper.

        The decorator allows you to mark a function
        as a custom script for sqlalchemy. Using
        this mechanism, you can conveniently call
        the desired set of actions in the right place.
        """
        raise NotImplementedError("This method should be redefined in the subclass")
