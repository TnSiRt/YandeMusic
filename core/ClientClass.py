import asyncio
from yandex_music import ClientAsync

YANDEX_TOKEN = "y0__xDRncmmCBje-AYg3qv_phQ9IL2RORzSlsEz9DVKg9xqkxqvKg"

class YandexAPI:
    def __init__(self, token: str = YANDEX_TOKEN):
        self.token = token
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.client = None

    async def _init_client(self):
        self.client = await ClientAsync(self.token).init()

    def init(self):
        """Запускаем инициализацию клиента"""
        return self.loop.run_until_complete(self._init_client())

    def search(self, query: str):
        """Обёртка над async search → возвращает результат синхронно"""
        return self.loop.run_until_complete(self._search(query))

    def get_likes(self):
        return self.loop.run_until_complete(self._get_like())

    async def _get_like(self):
        result = await self.client.users_likes_tracks()
        treacks = []
        for treack in result:
            data = await treack.fetch_track_async()
            add_data = {
                "title":data['title'],
                "artists":data['artists']['name'],
                "image":data['cover_uri'],
                "duration":data['duration_ms']
            }
            treacks.append(add_data)
        return treacks

    async def _search(self, query: str):
        result = await self.client.search(query)
        tracks = []
        if result.tracks:
            for track in result.tracks.results[:5]:
                artist = track.artists[0].name if track.artists else "Unknown"
                tracks.append(f"{artist} - {track.title}")
        return tracks