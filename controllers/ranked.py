import asyncio

from loguru import logger
from sqlalchemy import func, desc, select, asc, text

from controllers.base import CONTROLLER
from models.profile import Profile
from models.scores import Scores


class RankedController(CONTROLLER):
    def __init__(self):
        super().__init__()

    def get_connection(self):
        super().get_connection()

    def close_connection(self):
        super().close_connection()

    def _get_ranked(self, guild_id: int, limit: int = 10):
        self.get_connection()
        try:
            result = self.session.execute(
                select(
                    Profile.id,
                    Profile.user_id,
                    Profile.nick_name,
                    Profile.level,
                    func.sum(Scores.value).label("total_score")
                )
                .join(Profile)
                .where(Profile.guild_id == guild_id)  # type: ignore
                .where(Scores.profile_id == Profile.id)  # type: ignore
                .where(Profile.nick_name.isnot(None))  # type: ignore
                .where(Scores.created_at >= func.current_timestamp() - text("INTERVAL '8 days'"))  # expire in 8 days
                .group_by(Profile.id, Profile.user_id)
                .order_by(desc("total_score"), asc("id"))
                .limit(limit)
            )
            return result
        except Exception as e:
            logger.error(f"Error in get_ranked: {e}")
            raise e
        finally:
            self.close_connection()

    async def get_ranked(self, interaction, limit: int = 10):
        return await asyncio.to_thread(self._get_ranked, interaction, limit)
