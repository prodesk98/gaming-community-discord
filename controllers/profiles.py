import asyncio
from typing import Any, List, Type

from controllers.base import CONTROLLER
from models.profile import Profile

from loguru import logger


class ProfileController(CONTROLLER):
    def __init__(self):
        super().__init__()

    def get_connection(self):
        super().get_connection()

    def close_connection(self):
        super().close_connection()

    def _add_profile(self, instance: Type[Profile]) -> None:
        self.get_connection()
        try:
            self.session.add(instance)
            self.session.commit()
        except Exception as e:
            logger.error(f'Error adding profile: {e}')
            self.session.rollback()
            raise e
        finally:
            self.close_connection()

    def _update_profile(self, instance: Type[Profile]) -> None:
        self.get_connection()
        try:
            self.session.merge(instance)
            self.session.commit()
        except Exception as e:
            logger.error(f'Error updating profile: {e}')
            self.session.rollback()
            raise e
        finally:
            self.close_connection()

    def update(self, instance: Type[Profile]) -> None:
        self.get_connection()
        try:
            self.session.merge(instance)
            self.session.commit()
        except Exception as e:
            logger.error(f'Error updating profile: {e}')
            self.session.rollback()
            raise e
        finally:
            self.close_connection()

    def _remove_nickname(self, user_id: int, guild_id: int) -> None:
        self.get_connection()
        try:
            profile = self.session.query(Profile).filter_by(user_id=user_id, guild_id=guild_id).scalar()
            if profile is not None:
                profile.nick_name = None
                self.session.commit()
        except Exception as e:
            logger.error(f'Error removing nickname: {e}')
            raise e
        finally:
            self.close_connection()

    def _query(self, **kwargs) -> Any | None:
        self.get_connection()
        try:
            result = self.session.query(Profile).filter_by(**kwargs).scalar()
            return result
        except Exception as e:
            logger.error(f'Error querying profile: {e}')
            raise e
        finally:
            self.close_connection()

    def _remove(self, **kwargs) -> None:
        self.get_connection()
        try:
            self.session.query(Profile).filter_by(**kwargs).delete()
            self.session.commit()
        except Exception as e:
            logger.error(f'Error removing profile: {e}')
            self.session.rollback()
            raise e
        finally:
            self.close_connection()

    def get_profiles(self, **kwargs) -> List[Type[Profile]]:
        self.get_connection()
        try:
            result = self.session.query(Profile).filter_by(**kwargs).all()
            return result
        except Exception as e:
            logger.error(f'Error getting profiles: {e}')
            raise e
        finally:
            self.close_connection()

    async def query(self, **kwargs) -> Any:
        return await asyncio.to_thread(self._query, **kwargs)

    async def remove(self, **kwargs) -> None:
        return await asyncio.to_thread(self._remove, **kwargs)

    async def add_profile(self, instance: Type[Profile] | Profile) -> None:
        return await asyncio.to_thread(self._add_profile, instance)

    async def update_profile(self, instance: Type[Profile]) -> None:
        return await asyncio.to_thread(self._update_profile, instance)

    async def remove_nickname(self, user_id: int, guild_id: int) -> None:
        return await asyncio.to_thread(self._remove_nickname, user_id, guild_id)
