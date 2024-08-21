"""Module "database".

File:
    database.py

About:
    File describing the Databse and AsyncDatabase classes.
"""

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import (
    Session,
    sessionmaker,
    declarative_base,
    DeclarativeBase,
)
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession


BaseModel = declarative_base()


class Database:
    """SQLA Database class."""

    def __init__(self, connection_uri: str, debug: bool = False) -> None:
        self._engine = create_engine(
            connection_uri,
            echo=debug,
            pool_pre_ping=True,
        )
        self._session = sessionmaker(
            bind=self._engine,
            autoflush=False,
            class_=Session,
        )

    def create_tables(self, base: DeclarativeBase):
        """Creates all tables defined in the provided
        SQLAlchemy base model.

        Args:
            base (Any): The base model containing
            metadata for tables to be created.
        """

        metadata = base.metadata
        metadata.create_all(self._engine)

    def drop_tables(self, base: DeclarativeBase):
        """Drops all tables defined in the provided
        SQLAlchemy base model.

        Args:
            base (Any): The base model containing
            metadata for tables to be dropped.
        """

        metadata = base.metadata
        metadata.drop_all(self._engine)

    def make_session(self) -> Session:
        """Creates and returns a new SQLAlchemy session.

        Returns:
            Session: A new SQLAlchemy session.
        """

        return self._session()

    @property
    def engine(self) -> Engine:
        """Returns the SQLAlchemy engine instance.

        Returns:
            Engine: The SQLAlchemy engine instance.
        """

        return self._engine


class AsyncDatabase:
    """SQLA async Database class."""

    def __init__(self, connection_uri: str, debug: bool = False) -> None:
        self._engine = create_async_engine(
            connection_uri,
            echo=debug,
            pool_pre_ping=True,
        )
        self._session = sessionmaker(
            bind=self._engine,
            autoflush=False,
            class_=AsyncSession,
        )

    async def create_tables(self, base: DeclarativeBase):
        """Creates all tables defined in the provided
        SQLAlchemy base model.

        Args:
            base (Any): The base model containing
            metadata for tables to be created.
        """

        metadata = base.metadata
        async with self._engine.begin() as connection:
            await connection.run_sync(metadata.create_all)

    async def drop_tables(self, base: DeclarativeBase):
        """Drops all tables defined in the provided
        SQLAlchemy base model.

        Args:
            base (Any): The base model containing
            metadata for tables to be dropped.
        """

        metadata = base.metadata
        async with self._engine.begin() as connection:
            await connection.run_sync(metadata.drop_all)

    def make_session(self) -> AsyncSession:
        """Creates and returns a new SQLAlchemy async session.

        Returns:
            AsyncSession: A new SQLAlchemy async session.
        """

        return self._session()

    @property
    def engine(self) -> AsyncEngine:
        """Returns the SQLAlchemy async engine instance.

        Returns:
            AsyncEngine: The SQLAlchemy async engine instance.
        """

        return self._engine
