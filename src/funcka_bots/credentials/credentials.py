"""Module "credentials".

File:
    credentials.py

About:
    File describing data structures for storing
    credentials and setup configurations for any
    connections.
"""

from typing import NamedTuple


class AlchemyCredentials(NamedTuple):
    """Represents the credentials required to connect to a SQLAlchemy DBMS.

    :param str host: The hostname of the server.
    :param int port: The port number on which the server is listening.
    :param str user: The username for authentication.
    :param str pswd: The password for authentication.
    """

    host: str
    port: int
    user: str
    pswd: str


class AlchemySetup(NamedTuple):
    """Represents the setup configuration for a SQLAlchemy database.

    :param str dialect: The database dialect (e.g., `mysql`, `postgresql`).
    :param str driver:  The database driver (e.g., `pymysql`, `psycopg2`).
    :param str database: The name of the database.
    """

    dialect: str
    driver: str
    database: str


class RedisCredentials(NamedTuple):
    """Represents the credentials required to connect to a Redis server.

    :param str host: The hostname of the server.
    :param int port: The port number on which the server is listening.
    :param int db: The database number.
    """

    host: str
    port: int
    db: int


class RabbitMQCredentials(NamedTuple):
    """Represents the credentials required to connect to a RabbitMQ.

    :param str host: The hostname of the server.
    :param str vhost: The RabbitMQ virtual host.
    :param int port: The port number on which the server is listening.
    :param str user: The username for authentication.
    :param str pswd: The password for authentication.
    """

    vhost: str
    host: str
    port: int
    user: str
    pswd: str
