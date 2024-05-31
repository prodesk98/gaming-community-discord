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

    def _update_profile(self, instance: Profile) -> None:
        self.get_connection()
        self.session.merge(instance)
        self.session.commit()
        self.session.close()

    def _remove_nickname(self, user_id: int, guild_id: int) -> None:
        self.get_connection()
        profile = self.session.query(Profile).filter_by(user_id=user_id, guild_id=guild_id).scalar()
        if profile is not None:
            profile.nick_name = None
            self.session.commit()
        self.session.close()

    def _query(self, **kwargs) -> Any:
        self.get_connection()
        # has existing nick
        result = self.session.query(Profile).filter_by(**kwargs).scalar()
        self.session.close()
        return result

    def _remove(self, **kwargs) -> None:
        self.get_connection()
        self.session.query(Profile).filter_by(**kwargs).delete()
        self.session.commit()
        self.session.close()

    async def query(self, **kwargs) -> Any:
        return await asyncio.to_thread(self._query, **kwargs)

    async def remove(self, **kwargs) -> None:
        return await asyncio.to_thread(self._remove, **kwargs)

    async def add_profile(self, instance: Profile) -> None:
        return await asyncio.to_thread(self._add_profile, instance)

    async def update_profile(self, instance: Profile) -> None:
        return await asyncio.to_thread(self._update_profile, instance)

    async def remove_nickname(self, user_id: int, guild_id: int) -> None:
        return await asyncio.to_thread(self._remove_nickname, user_id, guild_id)
