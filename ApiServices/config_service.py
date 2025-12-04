"""
Service for handling configuration data.
"""
from typing import Dict, Any
from config import Config


class ConfigService:
    """Handles configuration data for the frontend."""
    
    def __init__(self, config: Config):
        self.config = config
    
    async def get_config(self) -> Dict[str, Any]:
        """Get frontend configuration."""
        return {
            "myName": self.config.my_name,
            "anniversaryDate": self.config.anniversary_date,
            "googleMapsApiKey": self.config.google_maps_api_key,
            "googleMapsZoom": self.config.google_maps_zoom,
            "googleMapsStyle": self.config.google_maps_style,
            "location": {
                "latitude": self.config.location_latitude,
                "longitude": self.config.location_longitude
            },
            "leftWidgets": self.config.left_widgets,
            "rightWidgets": self.config.right_widgets
        }
