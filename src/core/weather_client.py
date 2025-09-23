import httpx
from src.core.config import configs

class WeatherApiClient:
    BASE_URL = "http://api.weatherapi.com/v1/current.json"

    def __init__(self, http_client: httpx.AsyncClient):
        self.api_key = configs.WEATHER_API_KEY
        self.http_client = http_client

    async def get_weather(self, location: str = "New York"):
        params = {
            "key": self.api_key,
            "q": location,
            "aqi": "no"
        }
        resp = await self.http_client.get(self.BASE_URL, params=params)
        resp.raise_for_status()
        return resp.json()
