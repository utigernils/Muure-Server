"""
FastAPI server for handling web requests and managing API services.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from ApiServices.weather_service import WeatherService
from ApiServices.transport_service import TransportService
from ApiServices.quote_service import QuoteService
from ApiServices.calendar_service import CalendarService
from ApiServices.spotify_service import SpotifyService
from ApiServices.position_service import PositionService
from ApiServices.config_service import ConfigService
from ApiServices.frontend_service import FrontendService
from config_reader import Config
from state_manager import StateManager


class APIServer:
    """Manages the FastAPI server and routes."""
    
    def __init__(self, config: Config):
        self.config = config
        self.state_manager = StateManager()
        self.app = FastAPI(title="Muure Backend API")
        
        self.weather_service = WeatherService(config)
        self.transport_service = TransportService(config)
        self.quote_service = QuoteService(config)
        self.calendar_service = CalendarService(config)
        self.spotify_service = SpotifyService(config)
        self.position_service = PositionService(config)
        self.config_service = ConfigService(config, self.state_manager)
        self.frontend_service = FrontendService()
    
        self._setup_cors()
        self._setup_routes()
        self._mount_frontend()
    
    def _setup_cors(self):
        """Configure CORS middleware."""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def _setup_routes(self):
        """Setup API endpoints."""
        
        @self.app.get("/api/config")
        async def get_config():
            """Get web configuration."""
            try:
                data = await self.config_service.get_config()
                return data
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))  
        
        @self.app.get("/api/weather/current")
        async def get_current_weather():
            """Get current weather data."""
            try:
                data = await self.weather_service.get_current_weather()
                return data
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/api/weather/forecast")
        async def get_weather_forecast():
            """Get weather forecast data."""
            try:
                data = await self.weather_service.get_weather_forecast()
                return data
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/api/transport/departures")
        async def get_departures():
            """Get transport departures."""
            try:
                data = await self.transport_service.get_departures()
                return data
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/api/quote")
        async def get_quote():
            """Get a random quote."""
            try:
                data = await self.quote_service.get_quote()
                return data
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/api/calendar/events")
        async def get_calendar_events():
            """Get calendar events for today or next day with events."""
            try:
                data = await self.calendar_service.get_calendar_events()
                return data
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/api/spotify/now-playing")
        async def get_now_playing():
            """Get currently playing Spotify track."""
            try:
                data = await self.spotify_service.get_currently_playing()
                if data is None:
                    return {"is_playing": False}
                return data
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/api/position")
        async def get_position():
            """Get current position data."""
            try:
                data = await self.position_service.get_position()
                return data
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/api/widgets/left/next")
        async def next_left_widget():
            """Switch to next left widget."""
            try:
                self.state_manager.next_left_widget()
                return {"success": True, "widget": self.state_manager.get_left_widget()}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/api/widgets/right/next")
        async def next_right_widget():
            """Switch to next right widget."""
            try:
                self.state_manager.next_right_widget()
                return {"success": True, "widget": self.state_manager.get_right_widget()}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
    
    def _mount_frontend(self):
        """Mount web static files."""
        try:
            self.frontend_service.mount_frontend(self.app)
        except FileNotFoundError as e:
            print(f"Warning: {e}")
    
    def start(self):
        """Start the server."""
        host = self.config.server_host
        port = self.config.server_port
        print(f"Starting server on {host}:{port}")
        uvicorn.run(self.app, host=host, port=port)
