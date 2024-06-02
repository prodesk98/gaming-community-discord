import asyncio

from loguru import logger

from controllers.base import CONTROLLER
from models.scores import Scores

from sqlalchemy import func, text

from models.weekly import Weekly
from schemas.stats import StatsORM


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
            return result if result is not None else 0
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

    def get_weekly(self, profile_id: int) -> Weekly | None:
        self.get_connection()
        try:
            # selecionar a data de inicio da semana
            result = self.session.query(Weekly).filter(
                Weekly.created_at >= func.current_timestamp() - text("INTERVAL '8 days'"),
                Weekly.profile_id == profile_id  # type: ignore
            ).first()
            return result
        except Exception as e:
            logger.error("Error getting weekly: %s" % e)
            raise e
        finally:
            self.close_connection()

    def insert_weekly(self, stats: StatsORM, profile_id: int):
        self.get_connection()
        try:
            weekly = Weekly(
                profile_id=profile_id,
                level=stats.level,
                kills=stats.kills,
                wons=stats.wins,
                losses=stats.losses,
                assist=stats.assists,
            )
            self.session.add(weekly)
            self.session.commit()
        except Exception as e:
            logger.error("Error inserting weekly: %s" % e)
            self.session.rollback()
            raise e
        finally:
            self.close_connection()

    async def get_scores_by_user_id(self, profile_id: int) -> int:
        return await asyncio.to_thread(self._get_scores_by_user_id, profile_id)

    async def aadd_score(self, profile_id: int, value: int):
        return await asyncio.to_thread(self.add_score, profile_id, value)
