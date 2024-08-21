"""Module "database".

File:
    connection.py

About:
    File describing connection uri builder functions.
"""

from urllib.parse import quote
from funcka_bots.credentials import AlchemySetup, AlchemyCredentials


def build_connection_uri(setup: AlchemySetup, creds: AlchemyCredentials) -> str:
    """Builds a SQLAlchemy connection URI from the provided setup and credentials.

    Args:
        setup (AlchemySetup): The configuration settings for the database connection.
        creds (AlchemyCredentials): The credentials required for the database connection.

    Returns:
        str: A formatted connection URI for SQLAlchemy.
    """

    return (
        f"{setup.dialect}+{setup.driver}://"
        f"{quote(creds.user)}:{quote(creds.pswd)}@"
        f"{creds.host}:{creds.port}/"
        f"{setup.database}"
    )


def build_sqlite_uri(db_name: str, use_async_driver: bool = False) -> str:
    """Creates a SQLAlchemy connection URI to the SQLite database.

    Args:
        db_name (str): Name of database file.
        use_async_driver (bool, optional): Uses an asynchronous driver if enabled. Defaults to False.

    Returns:
        str: A formatted connection URI for SQLAlchemy.
    """
    return f"sqlite{'+aiosqlite' if use_async_driver else ''}:///{db_name}.db"
