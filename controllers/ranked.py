import asyncio

from sqlalchemy import func, desc, select, asc

from controllers.base import CONTROLLER
from databases.session import get_session
from models.profile import Profile
from models.scores import Scores


class RankedController(CONTROLLER):
    def __init__(self):
        super().__init__()

    def get_connection(self):
        if self.session is not None and self.session.is_active:
            return self.session
        self.session = get_session()

    def _get_ranked(self, guild_id: int, limit: int = 10):
        self.get_connection()
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
            .group_by(Profile.id, Profile.user_id)
            .order_by(desc("total_score"), asc("id"))
            .limit(limit)
        )
        self.session.close()
        return result

    async def get_ranked(self, interaction, limit: int = 10):
        return await asyncio.to_thread(self._get_ranked, interaction, limit)
