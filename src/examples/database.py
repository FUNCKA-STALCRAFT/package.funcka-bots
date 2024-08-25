from sqlalchemy.orm import declarative_base, Mapped, mapped_column, Session
from sqlalchemy.types import INTEGER, TEXT
from funcka_bots.database import SyncDB
from funcka_bots.database import build_sqlite_uri


# First, we create a database instance,
# which will allow us to interact with SQLite.

db_instance = SyncDB(connection_uri=build_sqlite_uri(), debug=False)

# Next, we create a basic one in the classic way
# ORM table model via SQLAlchemy.

BaseModel = declarative_base()


# # After which it is inherited from the base model
# when creating table models. This mechanism
# does not depend on the library.


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(TEXT(255))


# In order to interact with DBMS
# through ORM models, you need to register some kind of
# logic. The logic will be implemented through scripts,
# automatically opening and closing SQLAlchemy sessions.
# And in case of an error - a rollback.


@db_instance.script(auto_commit=False, debug=True)
def get_user(session: Session, user_id: int) -> str | None:
    user = session.get(User, {"id": user_id})
    return user if user is None else user.name


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
    get_user(25)
