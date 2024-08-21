"""Module "database".

File:
    __init__.py

About:
    Initializing the "database" module.
"""

from .connection import build_connection_uri, build_sqlite_uri
from .database import Database, BaseModel, AsyncDatabase
from .scripts import script, async_script


__all__ = (
    "build_connection_uri",  # A function to build SQLAlchemy connection URI.
    "build_sqlite_uri",
    "script",  # A decorator to mark functions as custom scripts for SQLAlchemy.
    "async_script",
    "Database",  # Class encapsulating SQLAlchemy database management operations.
    "AsyncDatabase",
    "BaseModel",  # Base class for SQLAlchemy models.
)
