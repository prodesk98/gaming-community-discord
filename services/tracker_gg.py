import asyncio

import requests
from schemas.stats import Root as Stats

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
        response = requests.get(url, headers=HEADERS, proxies=PROXIES)
        print(response.content)
        if not response.ok:
            return
        data = response.json()
        if not data:
            return
        return Stats(**data)

    async def get_profile_stats(self, nickname: str, platform: str) -> None | Stats:
        return await asyncio.to_thread(self._get_profile_stats, nickname, platform)

    def get_profile_stats_sync(self, nickname: str, platform: str) -> None | Stats:
        return self._get_profile_stats(nickname, platform)
