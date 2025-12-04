"""
Service for serving frontend static files.
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path


class FrontendService:
    """Handles serving the frontend static files."""
    
    def __init__(self, frontend_path: str = "ApiServices/frontend"):
        self.frontend_path = Path(frontend_path)
    
    def mount_frontend(self, app: FastAPI):
        """Mount the frontend static files to the app."""
        if self.frontend_path.exists():
            app.mount("/", StaticFiles(directory=str(self.frontend_path), html=True), name="frontend")
        else:
            raise FileNotFoundError(f"Frontend directory not found: {self.frontend_path}")
