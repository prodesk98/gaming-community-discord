import asyncio
import json
import re

import requests
from loguru import logger
from lxml import etree
from schemas.stats import Root as Stats, StatsORM
from config import CF_RESOLVER_URL, PROXY_IP

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


class TrackerGGService:
    @staticmethod
    def _cf_resolve(url: str) -> bytes | str | None:
        headers = {"Content-Type": "application/json"}
        data = {
            "cmd": "request.get",
            "url": url,
            "maxTimeout": 60000,
            "proxy": {
                "url": PROXY_IP,
            },
            "cookies": []
        }
        resp = requests.post(CF_RESOLVER_URL, headers=headers, json=data)
        if not resp.ok:
            return
        data = json.loads(resp.content)
        if data.get("status") != "ok":
            return
        return data.get("solution", {}).get("response", "")

    def _get_profile_stats(self, nickname: str, platform: str) -> None | Stats:
        url = f'{TRACKER_GG_API_ENDPOINT}/{GAME}/standard/matches/{platform}/{nickname}'
        response = self._cf_resolve(url)
        data = json.loads(response)
        if data is None:
            return
        return Stats(**data)

    def _get_profile_site(self, nickname: str, platform: str) -> StatsORM | None:
        url = f'https://tracker.gg/{GAME}/profile/{platform}/{nickname}/overview'
        response = self._cf_resolve(url)
        if response is None:
            return

        soup = BeautifulSoup(response, 'html.parser')
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

        return StatsORM(
            level=int(level),
            matches=int(matches),
            wins=int(matches_won),
            losses=int(matches_losses),
            kills=int(kills),
            assists=int(assists),
            score=float(score),
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
    stats = track.get_profile_site('oneniick', 'ubi')
    print(stats)
