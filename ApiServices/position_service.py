"""
Position service for fetching current position data.
"""
from typing import Dict, Any

from config import Config


class PositionService:
    """Handles position-related data."""
    
    def __init__(self, config: Config):
        self.config = config
    
    async def get_position(self) -> Dict[str, Any]:
        """Fetch current position data (mock implementation)."""
        # Mock position data - replace with real GPS/location service later
        return {
            "latitude": self.config.location_latitude,
            "longitude": self.config.location_longitude,
            "accuracy": 10.0,  # meters
            "timestamp": None  # Could add actual timestamp if needed
        }
