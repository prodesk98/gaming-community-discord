import asyncio
import re

import requests
from lxml import etree
from schemas.stats import Root as Stats, StatsORM

from bs4 import BeautifulSoup


TRACKER_GG_API_ENDPOINT = 'https://api.tracker.gg/api/v2'
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Priority": "u=1",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache"
}
GAME = 'xdefiant'
PROXIES = {
    "https": "http://199.167.236.12:3128"
}


class TrackerGGService:
    @staticmethod
    def _get_profile_stats(nickname: str, platform: str) -> None | Stats:
        url = f'{TRACKER_GG_API_ENDPOINT}/{GAME}/standard/matches/{platform}/{nickname}'
        response = requests.get(url, headers=HEADERS, proxies=PROXIES, timeout=10)
        if not response.ok:
            raise Exception(f'Error: {response.status_code}')
        data = response.json()
        if not data:
            return
        return Stats(**data)

    @staticmethod
    def _get_profile_site(nickname: str, platform: str) -> StatsORM | None:
        url = f'https://tracker.gg/{GAME}/profile/{platform}/{nickname}/overview'
        response = requests.get(url, headers=HEADERS, proxies=PROXIES, timeout=10)
        if not response.ok:
            return

        soup = BeautifulSoup(response.content, 'html.parser')
        dom = etree.HTML(str(soup))
        _level = next(iter(dom.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[3]/div/div/div[1]/div[1]/div/div/div/div/div'))).text
        level = re.sub(r'\D', '', _level)
        _matches = next(iter(dom.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[3]/div/div/div[1]/div[1]/div/div/div/div/span[2]'))).text
        matches = re.sub(r'\D', '', _matches)
        matches_won = next(iter(dom.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[3]/div/div/div[1]/div[2]/div[3]/div/div[2]/span[2]/span'))).text
        matches_losses = str(int(matches) - int(matches_won))
        _kills = next(iter(dom.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[3]/div/div/div[1]/div[2]/div[4]/div/div[2]/span[2]/span'))).text
        kills = re.sub(r'\D', '', _kills.replace(',', ''))
        _score = next(iter(dom.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[3]/div/div/div[1]/div[4]/div[3]/div/div[2]/span[2]/span[1]'))).text
        score = re.sub(r'\D', '', _score.replace(',', ''))
        _assists = next(iter(dom.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[3]/div/div/div[1]/div[4]/div[1]/div/div[2]/span[2]/span[1]'))).text
        assists = re.sub(r'\D', '', _assists.replace(',', ''))
        _mvp = next(iter(dom.xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[3]/div/div/div[1]/div[4]/div[2]/div/div[2]/span[2]/span'))).text
        mvp = re.sub(r'\D', '', _mvp.replace(',', ''))

        return StatsORM(
            level=int(level),
            matches=int(matches),
            wins=int(matches_won),
            losses=int(matches_losses),
            kills=int(kills),
            score=float(score),
            assists=int(assists),
            mvpCount=int(mvp)
        )

    async def get_profile_stats(self, nickname: str, platform: str) -> None | Stats:
        return await asyncio.to_thread(self._get_profile_stats, nickname, platform)

    async def aget_profile_site(self, nickname: str, platform: str) -> None | StatsORM:
        return await asyncio.to_thread(self._get_profile_site, nickname, platform)

    def get_profile_stats_sync(self, nickname: str, platform: str) -> None | Stats:
        return self._get_profile_stats(nickname, platform)

    def get_profile_site(self, nickname: str, platform: str) -> None | str:
        return self._get_profile_site(nickname, platform)


if __name__ == "__main__":
    track = TrackerGGService()
    track.get_profile_site('goncalves73', 'ubi')
