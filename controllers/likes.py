import asyncio

from controllers.base import CONTROLLER
from databases.session import get_session
from models.likes import Likes


class LikesController(CONTROLLER):
    def __init__(self):
        super().__init__()

    def get_connection(self):
        if self.session is not None and self.session.is_active:
            return self.session
        self.session = get_session()

    def _add_like(self, instance: Likes) -> None:
        self.get_connection()
        self.session.add(instance)
        self.session.commit()
        self.session.close()

    def _get_likes_by_target_id(self, target_id: int) -> int:
        self.get_connection()
        result = self.session.query(Likes).filter_by(target_id=target_id).count()
        self.session.close()
        return result

    def _has_like(self, profile_id: int, target_id: int) -> bool:
        self.get_connection()
        result = self.session.query(Likes).filter_by(profile_id=profile_id, target_id=target_id).first()
        self.session.close()
        return result is not None

    async def add_like(self, instance: Likes) -> None:
        return await asyncio.to_thread(self._add_like, instance)

    async def get_likes_by_target_id(self, target_id: int) -> int:
        return await asyncio.to_thread(self._get_likes_by_target_id, target_id)

    async def has_like(self, profile_id: int, target_id: int) -> bool:
        return await asyncio.to_thread(self._has_like, profile_id, target_id)
