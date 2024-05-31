import asyncio

from loguru import logger

from controllers.base import CONTROLLER
from models.scores import Scores

from sqlalchemy import func


class ScoresController(CONTROLLER):
    def __init__(self):
        super().__init__()

    def get_connection(self):
        super().get_connection()

    def close_connection(self):
        super().close_connection()

    def _get_scores_by_user_id(self, profile_id: int) -> int:
        self.get_connection()
        try:
            result = self.session.query(func.sum(Scores.value)).filter(Scores.profile_id == profile_id).scalar()  # noqa
            return result
        except Exception as e:
            logger.error("Error getting scores by user id: %s" % e)
            raise e
        finally:
            self.close_connection()

    def add_score(self, profile_id: int, value: int):
        self.get_connection()
        try:
            score = Scores(profile_id=profile_id, value=value)
            self.session.add(score)
            self.session.commit()
        except Exception as e:
            logger.error("Error adding score: %s" % e)
            self.session.rollback()
            raise e
        finally:
            self.close_connection()

    async def get_scores_by_user_id(self, profile_id: int) -> int:
        return await asyncio.to_thread(self._get_scores_by_user_id, profile_id)
