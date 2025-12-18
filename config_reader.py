"""
Configuration manager for loading and managing environment variables.
"""
import os
import json
from dotenv import load_dotenv


class Config:
    """Manages all configuration settings from environment variables."""
    
    def __init__(self):
        load_dotenv()
        
        self.server_host = os.getenv("SERVER_HOST", "0.0.0.0")
        self.server_port = int(os.getenv("SERVER_PORT", "8000"))

        self.render_width = int(os.getenv("RENDER_WIDTH", "1920"))
        self.render_height = int(os.getenv("RENDER_HEIGHT", "1080"))
        
        self.openweather_api_key = os.getenv("OPENWEATHER_API_KEY", "")
        self.weather_city = os.getenv("WEATHER_CITY", "Lucerne")
        self.weather_units = os.getenv("WEATHER_UNITS", "metric")
        
        self.sbb_station_id = os.getenv("SBB_STATION_ID", "")
        self.sbb_max_departures = int(os.getenv("SBB_MAX_DEPARTURES", "5"))
        self.sbb_exclude_to = os.getenv("SBB_EXCLUDE_TO", "")
        
        self.quotes_language = os.getenv("QUOTES_LANGUAGE", "de")
        
        self.google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY", "")
        self.google_maps_zoom = int(os.getenv("GOOGLE_MAPS_ZOOM", "15"))
        self.google_maps_style = os.getenv("GOOGLE_MAPS_STYLE", "")
        
        self.location_latitude = float(os.getenv("LOCATION_LATITUDE", "47.532"))
        self.location_longitude = float(os.getenv("LOCATION_LONGITUDE", "7.588"))
        self.position_api_url = os.getenv("POSITION_API_URL", "")
        
        self.my_name = os.getenv("MY_NAME", "")
        self.anniversary_date = os.getenv("ANNIVERSARY_DATE", "")
        
        self.calendar_url = os.getenv("CALENDAR_URL", "")
        self.calendar_timezone = os.getenv("CALENDAR_TIMEZONE", "Europe/Zurich")
        
        self.spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID", "")
        self.spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET", "")
        self.spotify_refresh_token = os.getenv("SPOTIFY_REFRESH_TOKEN", "")
    
    def validate(self):
        """Validate that all required configuration values are set."""
        required = [
            ("OPENWEATHER_API_KEY", self.openweather_api_key),
            ("SBB_STATION_ID", self.sbb_station_id),
            ("GOOGLE_MAPS_API_KEY", self.google_maps_api_key),
            ("MY_NAME", self.my_name),
            ("ANNIVERSARY_DATE", self.anniversary_date),
        ]
        
        missing = [name for name, value in required if not value]
        
        if missing:
            raise ValueError(f"Missing required configuration: {', '.join(missing)}")
