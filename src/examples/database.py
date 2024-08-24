from sqlalchemy.orm import declarative_base, Mapped, mapped_column, Session
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR
from funcka_bots.database import Database, script
from funcka_bots.database import build_connection_uri
from .credentials import AlchemyCredentials, AlchemySetup


# First, we create a database instance,
# which will allow us to interact with MySQL.
# When building URIs for DBMS, we use creds and setup
#  that we prepared earlier in "examples/credentials.py "

db_instance = Database(
    connection_uri=build_connection_uri(
        setup=AlchemySetup,
        creds=AlchemyCredentials,
    ),
    debug=False,
)

# Next, we create a basic one in the classic way
# ORM table model via SQLAlchemy.

BaseModel = declarative_base()


# # After which it is inherited from the base model
# when creating table models. This mechanism
# does not depend on the library.


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(VARCHAR(255))


# In order to interact with DBMS
# through ORM models, you need to register some kind of
# logic. The logic will be implemented through scripts,
# automatically opening and closing SQLAlchemy sessions.
# And in case of an error - a rollback.


@script(auto_commit=False, debug=True)
def do_smt(session: Session) -> None:
    user = session.get(User, {"id": 25})
    print(user)


# Please note that the script also has the option to specify
# will the script commit the changes itself after completing
# its logic or not.


def main() -> None:
    # Creating all tables linked to the base model.
    db_instance.create_tables(base=BaseModel)

    # Now we can work with the database using prepared scripts.
    # IMPORTANT: Although we specified session: Session in the
    # arguments of the "do_smt" function (which is mandatory),
    # When calling the script itself, a database instance must
    # be submitted for input.
    do_smt(db_instance)
