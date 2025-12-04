"""
Transport API service for fetching public transport departure information.
"""
import httpx
from typing import Dict, Any, List

from config_reader import Config


class TransportService:
    """Handles transport/SBB API calls."""
    
    BASE_URL = "https://transport.opendata.ch/v1"
    
    def __init__(self, config: Config):
        self.config = config
        self.station_id = config.sbb_station_id
        self.max_departures = config.sbb_max_departures
        self.exclude_to = config.sbb_exclude_to
    
    async def get_departures(self) -> List[Dict[str, Any]]:
        """Fetch transport departures."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/stationboard",
                params={
                    "id": self.station_id,
                    "limit": self.max_departures
                }
            )
            response.raise_for_status()
            data = response.json()
            
            departures = []
            
            if "stationboard" in data and isinstance(data["stationboard"], list):
                for item in data["stationboard"]:
                    destination = item.get("to", "Unknown")
                    
                    # Filter out excluded destinations
                    if self.exclude_to and destination:
                        if self.exclude_to.lower() in destination.lower():
                            continue
                    
                    departures.append({
                        "name": item.get("number") or item.get("name", "Unknown"),
                        "category": item.get("category", ""),
                        "to": destination,
                        "departure": item.get("stop", {}).get("departure"),
                        "platform": item.get("stop", {}).get("platform", "?"),
                        "delay": item.get("stop", {}).get("delay", 0)
                    })
            
            return departures
