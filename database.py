import os
import peewee
from dotenv import load_dotenv
from fastapi import Depends
from contextvars import ContextVar


load_dotenv()

DATABASE_NAME = os.getenv("DATABASE_NAME")

db_state_default = {
    "closed": None,
    "conn": None,
    "ctx": None,
    "transaction": None

}
db_state = ContextVar("db_state", default=db_state_default.copy())


class PeeweeConnectionState(peewee._ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)

    def __getattr__(self, name):
        return self._stater.get[name]

    def __setattr__(self, name, value):
        self._state.get()[name] = value


db = peewee.SqliteDatabase(DATABASE_NAME, check_same_thread=False)
db._state = PeeweeConnectionState()


async def reset_db_state():
    db._state._state.set(db_state_default.copy())
    db._state.reset()


def get_db(db_state=Depends(reset_db_state)):
    try:
        db.connect()
        yield
    finally:
        if not db.is_closed():
            db.close()

