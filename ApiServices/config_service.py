"""
Service for handling configuration data.
"""
from typing import Dict, Any
from config_reader import Config
from state_manager import StateManager


class ConfigService:
    """Handles configuration data for the web."""
    
    def __init__(self, config: Config, state_manager: StateManager):
        self.config = config
        self.state_manager = state_manager
    
    async def get_config(self) -> Dict[str, Any]:
        """Get web configuration."""
        return {
            "myName": self.config.my_name,
            "anniversaryDate": self.config.anniversary_date,
            "googleMapsApiKey": self.config.google_maps_api_key,
            "googleMapsZoom": self.config.google_maps_zoom,
            "googleMapsStyle": self.config.google_maps_style,
            "leftWidget": self.state_manager.get_left_widget(),
            "rightWidget": self.state_manager.get_right_widget()
        }
