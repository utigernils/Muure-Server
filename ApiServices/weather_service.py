"""
Weather API service for fetching current weather and forecast data.
"""
import httpx
from typing import Dict, Any, List
from datetime import datetime

from config_reader import Config


class WeatherService:
    """Handles all weather-related API calls."""
    
    BASE_URL = "https://api.openweathermap.org/data/2.5"
    
    def __init__(self, config: Config):
        self.config = config
        self.api_key = config.openweather_api_key
        self.city = config.weather_city
        self.units = config.weather_units
    
    async def get_current_weather(self) -> Dict[str, Any]:
        """Fetch current weather data."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/weather",
                params={
                    "q": self.city,
                    "appid": self.api_key,
                    "units": self.units
                }
            )
            response.raise_for_status()
            data = response.json()
            
            # Format the response
            return {
                "temp": round(data["main"]["temp"]),
                "feels_like": round(data["main"]["feels_like"]),
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"].capitalize(),
                "icon": data["weather"][0]["icon"],
                "wind_speed": round(data["wind"]["speed"] * 3.6),  # Convert m/s to km/h
                "city": data["name"]
            }
    
    async def get_weather_forecast(self) -> List[Dict[str, Any]]:
        """Fetch weather forecast data."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/forecast",
                params={
                    "q": self.city,
                    "appid": self.api_key,
                    "units": self.units
                }
            )
            response.raise_for_status()
            data = response.json()
            
            # Group forecasts by day
            daily_forecasts = {}
            for item in data["list"]:
                dt = datetime.fromtimestamp(item["dt"])
                date_str = dt.strftime("%Y-%m-%d")
                
                if date_str not in daily_forecasts:
                    daily_forecasts[date_str] = []
                daily_forecasts[date_str].append(item)
            
            # Get today and next 3 days
            today = datetime.now().strftime("%Y-%m-%d")
            sorted_dates = sorted(daily_forecasts.keys())
            target_dates = [d for d in sorted_dates if d > today][:3]
            
            # If we don't have 3 future days, include today
            if len(target_dates) < 3:
                target_dates.insert(0, today)
                target_dates = target_dates[:3]
            
            # Process each day
            processed_forecast = []
            for date_str in target_dates:
                day_data = daily_forecasts.get(date_str, [])
                if not day_data:
                    continue
                
                temps = [item["main"]["temp"] for item in day_data]
                
                # Find midday forecast (around 12-14h)
                midday_forecast = None
                for item in day_data:
                    hour = datetime.fromtimestamp(item["dt"]).hour
                    if 12 <= hour <= 14:
                        midday_forecast = item
                        break
                
                if not midday_forecast:
                    midday_forecast = day_data[0]
                
                date = datetime.strptime(date_str, "%Y-%m-%d")
                day_name = "Today" if date_str == today else date.strftime("%a")
                
                processed_forecast.append({
                    "date": date_str,
                    "day": day_name,
                    "temp_max": round(max(temps)),
                    "temp_min": round(min(temps)),
                    "description": midday_forecast["weather"][0]["description"].capitalize(),
                    "icon": midday_forecast["weather"][0]["icon"],
                    "humidity": midday_forecast["main"]["humidity"],
                    "pop": round(midday_forecast.get("pop", 0) * 100)
                })
            
            return processed_forecast
