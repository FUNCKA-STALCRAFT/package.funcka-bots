"""Module "database".

File:
    scripts.py

About:
    File describing the SQLA script decorators.
"""

from typing import Callable, Optional, Any
from loguru import logger
from .database import Database, AsyncDatabase


def script(auto_commit: bool = True, debug: bool = False) -> Callable:
    """A decorator that implements a custom script wrapper.

    The decorator allows you to mark a function
    as a custom script for sqlalchemy. Using
    this mechanism, you can conveniently call
    the desired set of actions in the right place.
    """

    def decorator(func: Callable) -> Callable:
        def wrapper(db_instance: Database, *args, **kwargs) -> Optional[Any]:
            session = db_instance.make_session()
            try:
                result = func(session, *args, **kwargs)

                if auto_commit:
                    session.commit()

                return result

            except Exception as error:
                session.rollback()

                if debug:
                    _handle_exception(error, func)

            finally:
                session.close()

        return wrapper

    return decorator


def async_script(auto_commit: bool = True, debug: bool = False) -> Callable:
    """An async decorator that implements a custom script wrapper.

    The decorator allows you to mark an async
    function as a custom script for sqlalchemy.
    Using this mechanism, you can conveniently call
    the desired set of actions in the right place.
    """

    def decorator(func: Callable) -> Callable:
        async def wrapper(db_instance: AsyncDatabase, *args, **kwargs) -> Optional[Any]:
            session = db_instance.make_session()
            try:
                result = await func(session, *args, **kwargs)

                if auto_commit:
                    await session.commit()

                return result

            except Exception as error:
                await session.rollback()

                if debug:
                    _handle_exception(error, func)

            finally:
                await session.close()

        return wrapper

    return decorator


def _handle_exception(error: Exception, func: Callable) -> None:
    text = (
        f"Script <{func.__name__}> execution failed. "
        "Transaction rolled back. \n"
        f"ErrorMessage: {error}"
    )
    logger.error(text)
