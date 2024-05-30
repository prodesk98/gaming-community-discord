import asyncio
from typing import Any

from controllers.base import CONTROLLER
from databases.session import get_session
from models.profile import Profile


class ProfileController(CONTROLLER):
    def __init__(self):
        super().__init__()

    def get_connection(self):
        if self.session is not None and self.session.is_active:
            return self.session
        self.session = get_session()

    def _add_profile(self, instance: Profile) -> None:
        self.get_connection()
        self.session.add(instance)
        self.session.commit()
        self.session.close()

    def _query(self, **kwargs) -> Any:
        self.get_connection()
        # has existing nick
        result = self.session.query(Profile).filter_by(**kwargs).scalar()
        self.session.close()
        return result

    async def query(self, **kwargs) -> Any:
        return await asyncio.to_thread(self._query, **kwargs)

    async def add_profile(self, instance: Profile) -> None:
        return await asyncio.to_thread(self._add_profile, instance)
