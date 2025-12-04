"""
Display controller that coordinates rendering and hardware updates.
"""
import asyncio
from datetime import datetime
from pathlib import Path
from state_manager import StateManager
from render import Renderer
from HardwareServices.display_service import DisplayService
from config import Config


class DisplayController:
    """Coordinates display updates between renderer and hardware."""
    
    def __init__(self, config: Config, state_manager: StateManager, renderer: Renderer, display_service: DisplayService):
        self.config = config
        self.state_manager = state_manager
        self.renderer = renderer
        self.display_service = display_service
        self.output_file = "display.png"
    
    async def update_display(self, force: bool = False):
        """
        Update the display with current page configuration.
        
        Args:
            force: Force update even if content hasn't changed
        """
        try:
            current_page = self.state_manager.get_current_page()
            print(f"\n[UPDATE] Rendering page: {current_page['name']}")
            
            self._update_config_widgets(current_page)
            
            output_path = await self.renderer.render_to_png(self.output_file)
            print(f"[UPDATE] Render complete: {output_path}")
            
            self.display_service.refresh_screen(output_path)
            
            timestamp = datetime.now().isoformat()
            self.state_manager.update_timestamp(timestamp)
            
            print(f"[UPDATE] Display update successful\n")
            
        except Exception as e:
            print(f"[ERROR] Display update failed: {e}")
    
    def _update_config_widgets(self, page: dict):
        """Update config with current page's widget configuration."""
        self.config.left_widgets = page.get("left_widgets", [])
        self.config.right_widgets = page.get("right_widgets", [])
