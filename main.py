"""
Main entry point for the Muure backend server.
Controls all services and starts the API server.
"""
from server import APIServer
from config import Config
from render import Renderer
from state_manager import StateManager
from display_controller import DisplayController
from scheduler_service import SchedulerService
from HardwareServices.display_service import DisplayService
from HardwareServices.buttons_service import ButtonService
import asyncio
import threading


class MuureClient:
    """Main controller for the Muure backend."""
    
    def __init__(self):
        self.config = Config()
        self.server = APIServer(self.config)
        self.renderer = Renderer(self.config)
        
        self.state_manager = StateManager()
        self.display_service = DisplayService()
        self.button_service = ButtonService()
        
        self.display_controller = DisplayController(
            self.config,
            self.state_manager,
            self.renderer,
            self.display_service
        )
        
        self.scheduler = SchedulerService(self.display_controller, interval_seconds=3)
        
        self.button_service.set_callbacks(
            on_next=self._handle_next_button,
            on_prev=self._handle_prev_button
        )
        
        self.server.set_button_service(self.button_service)
        self.event_loop = None
    
    def _handle_next_button(self):
        """Handle next button press."""
        print("\n[BUTTON] Next button pressed")
        self.state_manager.next_page()
        if self.event_loop:
            asyncio.run_coroutine_threadsafe(
                self.display_controller.update_display(force=True),
                self.event_loop
            )
    
    def _handle_prev_button(self):
        """Handle previous button press."""
        print("\n[BUTTON] Previous button pressed")
        self.state_manager.prev_page()
        if self.event_loop:
            asyncio.run_coroutine_threadsafe(
                self.display_controller.update_display(force=True),
                self.event_loop
            )
    
    async def start_services(self):
        """Start all async services."""
        print("Starting Muure services...")
        self.event_loop = asyncio.get_event_loop()
        
        button_task = asyncio.create_task(self.button_service.start_fake_buttons())
        scheduler_task = asyncio.create_task(self.scheduler.start())
        
        await asyncio.gather(button_task, scheduler_task)
    
    def run(self):
        """Start the backend server."""
        print("="*60)
        print("Starting Muure E-Ink Dashboard")
        print("="*60)
        
        def start_async_services():
            asyncio.run(self.start_services())
        
        services_thread = threading.Thread(target=start_async_services, daemon=True)
        services_thread.start()
        
        print("\nDebug Commands:")
        print("  - POST http://localhost:8000/api/buttons/next (trigger next page)")
        print("  - POST http://localhost:8000/api/buttons/prev (trigger prev page)")
        print("  - Or use: curl -X POST http://localhost:8000/api/buttons/next")
        print("="*60 + "\n")
        
        self.server.start()


if __name__ == "__main__":
    backend = MuureClient()
    backend.run()
