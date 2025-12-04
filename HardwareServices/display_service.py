"""
Display service for managing e-ink screen updates.
Fake implementation for debugging without hardware.
"""
from pathlib import Path
from datetime import datetime


class DisplayService:
    """Manages e-ink display hardware interface."""
    
    def __init__(self):
        self.last_refresh = None
        self.refresh_count = 0
    
    def refresh_screen(self, image_path: Path):
        """
        Refresh the e-ink display with new image.
        Fake implementation that just prints for debugging.
        """
        self.refresh_count += 1
        self.last_refresh = datetime.now()
        
        print(f"[DISPLAY] Screen refresh #{self.refresh_count}")
        print(f"[DISPLAY] Image: {image_path}")
        print(f"[DISPLAY] Time: {self.last_refresh.strftime('%H:%M:%S')}")
        print(f"[DISPLAY] {'='*50}")
    
    def clear_screen(self):
        """Clear the e-ink display."""
        print("[DISPLAY] Screen cleared")
    
    def get_refresh_count(self) -> int:
        """Get total number of refreshes."""
        return self.refresh_count
