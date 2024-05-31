import asyncio

from loguru import logger

from controllers.base import CONTROLLER
from models.likes import Likes


class LikesController(CONTROLLER):
    def __init__(self):
        super().__init__()

    def get_connection(self):
        super().get_connection()

    def close_connection(self):
        super().close_connection()

    def _add_like(self, instance: Likes) -> None:
        self.get_connection()
        try:
            self.session.add(instance)
            self.session.commit()
        except Exception as e:
            logger.error(f'Error adding like: {e}')
            self.session.rollback()
            raise e
        finally:
            self.close_connection()

    def _get_likes_by_target_id(self, target_id: int) -> int:
        self.get_connection()
        try:
            result = self.session.query(Likes).filter_by(target_id=target_id).count()
            return result
        except Exception as e:
            logger.error(f'Error getting likes by target_id: {e}')
            raise e
        finally:
            self.close_connection()

    def _has_like(self, profile_id: int, target_id: int) -> bool:
        self.get_connection()
        try:
            result = self.session.query(Likes).filter_by(profile_id=profile_id, target_id=target_id).first()
            return result is not None
        except Exception as e:
            logger.error(f'Error checking if like exists: {e}')
            raise e
        finally:
            self.close_connection()

    async def add_like(self, instance: Likes) -> None:
        return await asyncio.to_thread(self._add_like, instance)

    async def get_likes_by_target_id(self, target_id: int) -> int:
        return await asyncio.to_thread(self._get_likes_by_target_id, target_id)

    async def has_like(self, profile_id: int, target_id: int) -> bool:
        return await asyncio.to_thread(self._has_like, profile_id, target_id)
