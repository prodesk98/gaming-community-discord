import asyncio

from controllers.base import CONTROLLER
from databases.session import get_session
from models.scores import Scores

from sqlalchemy import func


class ScoresController(CONTROLLER):
    def __init__(self):
        super().__init__()

    def get_connection(self):
        if self.session is not None and self.session.is_active:
            return self.session
        self.session = get_session()

    def _get_scores_by_user_id(self, profile_id: int) -> int:
        self.get_connection()
        result = self.session.query(func.sum(Scores.value)).filter(Scores.profile_id == profile_id).scalar()  # noqa
        self.session.close()
        if result is None:
            return 0
        return result

    def add_score(self, profile_id: int, value: int):
        self.get_connection()
        score = Scores(profile_id=profile_id, value=value)
        self.session.add(score)
        self.session.commit()
        self.session.close()

    async def get_scores_by_user_id(self, profile_id: int) -> int:
        return await asyncio.to_thread(self._get_scores_by_user_id, profile_id)
