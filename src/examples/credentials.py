from funcka_bots.credentials import (
    AlchemyCredentials,
    AlchemySetup,
    RedisCredentials,
)


alchemy_creds = AlchemyCredentials(
    host="mysql.database.io",
    port=2206,
    user="cool_bot",
    pswd="cool_bot_secret_pswd",
)

alchemy_setup = AlchemySetup(
    dialect="mysql",
    driver="pymysql",
    database="test_schema",
)

redis_creds = RedisCredentials(
    host="my.redis.io",
    port=2263,
    db=0,
)
