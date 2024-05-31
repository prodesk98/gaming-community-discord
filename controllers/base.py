from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from databases.session import get_session


class CONTROLLER(ABC):
    def __init__(self):
        self.session: Session | None = None

    @abstractmethod
    def get_connection(self):
        self.session = get_session()

    @abstractmethod
    def close_connection(self):
        if self.session:
            self.session.close()
