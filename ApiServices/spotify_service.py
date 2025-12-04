"""
Spotify API service for fetching currently playing track information.
"""
import httpx
import base64
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

from config import Config


class SpotifyService:
    """Handles all Spotify-related API calls."""
    
    AUTH_URL = "https://accounts.spotify.com/api/token"
    API_URL = "https://api.spotify.com/v1"
    
    def __init__(self, config: Config):
        self.config = config
        self.client_id = config.spotify_client_id
        self.client_secret = config.spotify_client_secret
        self.refresh_token = config.spotify_refresh_token
        self.access_token = None
        self.token_expires_at = None
    
    async def _get_access_token(self) -> str:
        """Get or refresh the access token."""
        # Check if we have a valid token
        if self.access_token and self.token_expires_at:
            if datetime.now() < self.token_expires_at:
                return self.access_token
        
        # Refresh the token
        auth_str = f"{self.client_id}:{self.client_secret}"
        auth_bytes = auth_str.encode("utf-8")
        auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.AUTH_URL,
                headers={
                    "Authorization": f"Basic {auth_base64}",
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": self.refresh_token
                }
            )
            response.raise_for_status()
            data = response.json()
            
            self.access_token = data["access_token"]
            # Token expires in seconds, subtract 60s buffer
            expires_in = data.get("expires_in", 3600)
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in - 60)
            
            return self.access_token
    
    async def get_currently_playing(self) -> Optional[Dict[str, Any]]:
        """Fetch currently playing track data."""
        try:
            access_token = await self._get_access_token()
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.API_URL}/me/player/currently-playing",
                    headers={
                        "Authorization": f"Bearer {access_token}"
                    }
                )
                
                # No content means nothing is playing
                if response.status_code == 204:
                    return None
                
                response.raise_for_status()
                data = response.json()
                
                # Check if something is actually playing
                if not data or not data.get("is_playing"):
                    return None
                
                item = data.get("item")
                if not item:
                    return None
                
                # Get album art (prefer medium size, fallback to available)
                album_art_url = None
                if item.get("album") and item["album"].get("images"):
                    images = item["album"]["images"]
                    # Try to get 300x300 image, or largest available
                    if len(images) > 1:
                        album_art_url = images[1]["url"]
                    elif len(images) > 0:
                        album_art_url = images[0]["url"]
                
                # Get artists
                artists = [artist["name"] for artist in item.get("artists", [])]
                
                # Format the response
                return {
                    "is_playing": True,
                    "track_name": item.get("name", "Unknown Track"),
                    "artists": artists,
                    "album_name": item.get("album", {}).get("name", "Unknown Album"),
                    "album_art_url": album_art_url,
                    "duration_ms": item.get("duration_ms", 0),
                    "progress_ms": data.get("progress_ms", 0)
                }
        
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 204:
                return None
            raise
        except Exception as e:
            print(f"Error fetching Spotify data: {e}")
            return None
