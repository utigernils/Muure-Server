"""
Map service for generating and caching static map images.
"""
from pathlib import Path
import httpx

from config_reader import Config
from state_manager import StateManager
from ApiServices.position_service import PositionService


class MapService:
    """Handles static map images with position-based caching."""

    def __init__(self, config: Config, state_manager: StateManager, position_service: PositionService):
        self.config = config
        self.state_manager = state_manager
        self.position_service = position_service
        self.cache_path = Path("map_cache.png")

    async def get_map_image(self) -> bytes:
        """Return the map image, only refetching from Google when the position changed."""
        position = await self.position_service.get_position()
        latitude = round(position["latitude"], 5)
        longitude = round(position["longitude"], 5)

        last_position = self.state_manager.get_position()

        if (
            self.cache_path.exists()
            and last_position.get("latitude") == latitude
            and last_position.get("longitude") == longitude
        ):
            return self.cache_path.read_bytes()

        image_bytes = await self._fetch_static_map(latitude, longitude)

        self.cache_path.write_bytes(image_bytes)
        self.state_manager.set_position(latitude, longitude)

        return image_bytes

    async def _fetch_static_map(self, latitude: float, longitude: float) -> bytes:
        """Fetch a static map image from Google Maps."""
        url = (
            "https://maps.googleapis.com/maps/api/staticmap"
            f"?center={latitude},{longitude}"
            f"&zoom={self.config.google_maps_zoom}"
            "&size=640x480"
            f"&key={self.config.google_maps_api_key}"
            f"&markers=color:black|{latitude},{longitude}"
        )
        if self.config.google_maps_style:
            url += f"&map_id={self.config.google_maps_style}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.content
