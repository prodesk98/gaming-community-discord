from math import ceil
from time import sleep

from apscheduler.schedulers.blocking import BlockingScheduler
from loguru import logger

from commands.add_profile import tracker_gg_service
from controllers.profiles import ProfileController
from controllers.scores import ScoresController


def stats_job():
    profiles = ProfileController().get_profiles()

    for profile in profiles:
        if profile.nick_name is None:
            continue

        try:
            stats = tracker_gg_service.get_profile_site(profile.nick_name, 'ubi')
            if not stats:
                continue
        except Exception as e:
            logger.error(f"Error: {e}")
            continue

        # calculate xp
        # weights
        weight_kills = 2
        weight_wins = 1.2
        weight_assists = 1.5

        # calculate difference
        diff_kills = stats.kills - profile.kills
        diff_wins = stats.wins - profile.wins
        diff_assists = stats.assists - profile.assists

        # xp delta
        XPdelta = ceil(diff_kills * weight_kills + diff_wins * weight_wins + diff_assists * weight_assists)

        profile.level = stats.level
        profile.matches = stats.matches
        profile.wins = stats.wins
        profile.losses = stats.losses
        profile.kills = stats.kills
        profile.score = stats.score
        profile.assists = stats.assists
        ProfileController().update(profile)

        if XPdelta > 0:
            ScoresController().add_score(profile.id, XPdelta)  # type: ignore

        logger.info(f"Added {XPdelta} XP to {profile.nick_name}")
        logger.info(f"Updated {profile.nick_name} stats")
        logger.debug("Waiting 10 seconds")

        sleep(10)


stats_job()
scheduler = BlockingScheduler()
scheduler.add_job(stats_job, 'interval', minutes=15)

if __name__ == '__main__':
    scheduler.start()
