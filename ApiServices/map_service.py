"""
Map service for generating and caching static map images.
"""
from io import BytesIO
from pathlib import Path
from urllib.parse import quote_plus

import httpx
from PIL import Image, ImageDraw

from config_reader import Config
from state_manager import StateManager
from ApiServices.position_service import PositionService

ATTRIBUTION_HEIGHT = 24

MARKER_RADIUS = 10
MARKER_BORDER_WIDTH = 3


class MapService:
    """Handles static map images with position-based caching."""

    def __init__(self, config: Config, state_manager: StateManager, position_service: PositionService):
        self.config = config
        self.state_manager = state_manager
        self.position_service = position_service
        self.cache_path = Path("map_cache.png")

    async def get_map_image(self) -> bytes:
        """Return the map image, only refetching from Google when the location changed."""
        location = await self.position_service.get_location()

        if self.cache_path.exists() and self.state_manager.get_location() == location:
            return self.cache_path.read_bytes()

        image_bytes = await self._fetch_static_map(location)
        image_bytes = self._process_image(image_bytes)

        self.cache_path.write_bytes(image_bytes)
        self.state_manager.set_location(location)

        return image_bytes

    async def _fetch_static_map(self, location: str) -> bytes:
        """Fetch a static map image from Google Maps."""
        url = (
            "https://maps.googleapis.com/maps/api/staticmap"
            f"?center={quote_plus(location)}"
            f"&zoom={self.config.google_maps_zoom}"
            "&size=640x480"
            f"&key={self.config.google_maps_api_key}"
        )
        if self.config.google_maps_style:
            url += f"&map_id={self.config.google_maps_style}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.content

    def _process_image(self, image_bytes: bytes) -> bytes:
        """Remove the Google branding and draw a custom marker on the map."""
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
        width, height = image.size

        # The position is at the center of the fetched image.
        center_x = width // 2
        center_y = height // 2

        # Crop the Google attribution strip at the bottom.
        image = image.crop((0, 0, width, height - ATTRIBUTION_HEIGHT))

        # Draw a white circle with a black border at the position.
        draw = ImageDraw.Draw(image)
        draw.ellipse(
            [
                center_x - MARKER_RADIUS,
                center_y - MARKER_RADIUS,
                center_x + MARKER_RADIUS,
                center_y + MARKER_RADIUS,
            ],
            fill="white",
            outline="black",
            width=MARKER_BORDER_WIDTH,
        )

        output = BytesIO()
        image.save(output, format="PNG")
        return output.getvalue()
