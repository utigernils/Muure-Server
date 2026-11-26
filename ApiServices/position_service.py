"""
Location service for fetching the geocoded location from Home Assistant.
"""
import httpx

from config_reader import Config


class PositionService:
    """Handles location-related data."""
    
    def __init__(self, config: Config):
        self.config = config
    
    async def get_location(self) -> str:
        """Fetch the geocoded location from Home Assistant."""
        url = f"{self.config.homeassistant_url}/api/states/{self.config.homeassistant_sensor_id}"
        headers = {"Authorization": f"Bearer {self.config.homeassistant_api_key}"}
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                data = response.json()
                location = data.get("state", "").strip()
                if location and location not in ("unknown", "unavailable"):
                    return location
        except Exception as e:
            print(f"Error fetching location from Home Assistant: {e}")

        # Fallback to the configured coordinates.
        return f"{self.config.location_latitude},{self.config.location_longitude}"
