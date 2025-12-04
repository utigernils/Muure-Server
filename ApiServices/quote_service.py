"""
Quote API service for fetching random quotes.
"""
import httpx
from typing import Dict, Any

from config import Config


class QuoteService:
    """Handles quote API calls."""
    
    BASE_URL = "https://api.zitat-service.de/v1"
    
    def __init__(self, config: Config):
        self.config = config
        self.language = config.quotes_language
    
    async def get_quote(self) -> Dict[str, Any]:
        """Fetch a random quote."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/quote",
                params={
                    "language": self.language
                }
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "text": data.get("quote", ""),
                "author": data.get("authorName", "Unknown")
            }
