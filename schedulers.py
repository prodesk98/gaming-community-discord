from math import ceil
from time import sleep

from apscheduler.schedulers.blocking import BlockingScheduler
from loguru import logger

from commands.add_profile import tracker_gg_service
from controllers.profiles import ProfileController
from controllers.scores import ScoresController
from schemas.stats import StatsORM


def stats_job():
    profiles = ProfileController().get_profiles()

    for profile in profiles:
        if profile.nick_name is None:
            continue
        profile_stats = tracker_gg_service.get_profile_stats_sync(profile.nick_name, 'ubi')
        if not profile_stats:
            continue
        stats = StatsORM()
        stats.level = next(iter(next(iter(profile_stats.data.matches)).segments)).stats.playerLevel.value

        for match in profile_stats.data.matches:
            for segment in match.segments:
                if segment.type != 'overview':
                    continue
                stats.matches += segment.stats.matchesCompleted.value
                stats.wins += segment.stats.matchesWon.value
                stats.losses += segment.stats.matchesLost.value
                stats.kills += segment.stats.kills.value
                stats.score += segment.stats.score.value
                stats.assists += segment.stats.assists.value

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

        logger.info(f"Updated {profile.nick_name} stats")
        logger.debug("Waiting 10 seconds")

        sleep(10)


stats_job()
scheduler = BlockingScheduler()
scheduler.add_job(stats_job, 'interval', minutes=30)

if __name__ == '__main__':
    scheduler.start()
