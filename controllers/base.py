from abc import ABC, abstractmethod

from sqlalchemy.orm import Session


class CONTROLLER(ABC):
    def __init__(self):
        self.session: Session | None = None

    @abstractmethod
    def get_connection(self):
        pass
