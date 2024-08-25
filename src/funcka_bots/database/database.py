"""Module "database".

File:
    database.py

About:
    File describing the Sync and Async Database classes.
"""

from typing import Callable, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session, DeclarativeBase
from sqlalchemy import create_engine
from .base import BaseDB


class SyncDB(BaseDB):
    """SQLAlchemy Database class."""

    def __init__(self, connection_uri: str, debug: bool = False) -> None:
        super().__init__(
            engine_creation_func=create_engine,
            session_class=Session,
            connection_uri=connection_uri,
            debug=debug,
        )

    def create_tables(self, base: DeclarativeBase) -> None:
        metadata = base.metadata
        metadata.create_all(self._engine)

    def drop_tables(self, base: DeclarativeBase) -> None:
        metadata = base.metadata
        metadata.drop_all(self._engine)

    def script(self, auto_commit: bool = True, debug: bool = False) -> Callable:
        def decorator(func: Callable) -> Callable:
            def wrapper(*args, **kwargs) -> Optional[Any]:
                session = self.make_session()
                try:
                    result = func(session, *args, **kwargs)
                    if auto_commit:
                        session.commit()
                    return result

                except Exception as error:
                    session.rollback()
                    if debug:
                        self._handle_exception(error, func)

                finally:
                    session.close()

            return wrapper

        return decorator


class AsyncDB(BaseDB):
    """SQLA async Database class."""

    def __init__(self, connection_uri: str, debug: bool = False) -> None:
        super().__init__(
            engine_creation_func=create_async_engine,
            session_class=AsyncSession,
            connection_uri=connection_uri,
            debug=debug,
        )

    async def create_tables(self, base: DeclarativeBase):
        metadata = base.metadata
        async with self._engine.begin() as connection:
            await connection.run_sync(metadata.create_all)

    async def drop_tables(self, base: DeclarativeBase):
        metadata = base.metadata
        async with self._engine.begin() as connection:
            await connection.run_sync(metadata.drop_all)

    def script(self, auto_commit: bool = True, debug: bool = False) -> Callable:
        def decorator(func: Callable) -> Callable:
            async def wrapper(*args, **kwargs) -> Optional[Any]:
                session = self.make_session()
                try:
                    result = await func(session, *args, **kwargs)
                    if auto_commit:
                        await session.commit()
                    return result

                except Exception as error:
                    await session.rollback()
                    if debug:
                        self._handle_exception(error, func)

                finally:
                    await session.close()

            return wrapper

        return decorator
