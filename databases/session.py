from sqlalchemy.orm import Session
from .database import engine


def get_session() -> Session:
    session = Session(engine)
    return session
