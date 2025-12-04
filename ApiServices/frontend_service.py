"""
Service for serving web static files.
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path


class FrontendService:
    """Handles serving the web static files."""
    
    def __init__(self, frontend_path: str = "./web/"):
        self.frontend_path = Path(frontend_path)
    
    def mount_frontend(self, app: FastAPI):
        """Mount the web static files to the app."""
        if self.frontend_path.exists():
            app.mount("/", StaticFiles(directory=str(self.frontend_path), html=True), name="web")
        else:
            raise FileNotFoundError(f"Frontend directory not found: {self.frontend_path}")
