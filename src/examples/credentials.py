from funcka_bots.credentials import (
    AlchemyCredentials,
    AlchemySetup,
    RedisCredentials,
)


# # These data structures are based on NamedTuple
# in fact, they are DTO,
# with which you can quickly and conveniently
# transfer the connection\session data to the class
# databases\message broker\cache.

# # Perfect for defining them inside
# files like "config.py".


# Data for connecting to MySQL DBMS
alchemy_creds = AlchemyCredentials(
    host="mysql.database.io",
    port=2206,
    user="cool_bot",
    pswd="cool_bot_secret_pswd",
)

# Data for generating the database URL in SQLAlchemy
alchemy_setup = AlchemySetup(
    dialect="mysql",
    driver="pymysql",
    database="test_schema",
)

# Connection data to Redis
redis_creds = RedisCredentials(
    host="my.redis.io",
    port=2263,
    db=0,
)
