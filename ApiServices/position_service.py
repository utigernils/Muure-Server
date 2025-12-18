"""
Position service for fetching current position data.
"""
from typing import Dict, Any
import httpx

from config_reader import Config


class PositionService:
    """Handles position-related data."""
    
    def __init__(self, config: Config):
        self.config = config
    
    async def get_position(self) -> Dict[str, Any]:
        """Fetch current position data."""
        if self.config.position_api_url:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(self.config.position_api_url)
                    response.raise_for_status()
                    data = response.json()
                    return {
                        "latitude": data.get("latitude", self.config.location_latitude),
                        "longitude": data.get("longitude", self.config.location_longitude),
                        "accuracy": 10.0,
                        "timestamp": data.get("created_at")
                    }
            except Exception as e:
                print(f"Error fetching position: {e}")
                # Fallback to config

        # Mock position data - replace with real GPS/location service later
        return {
            "latitude": self.config.location_latitude,
            "longitude": self.config.location_longitude,
            "accuracy": 10.0,  # meters
            "timestamp": None  # Could add actual timestamp if needed
        }
