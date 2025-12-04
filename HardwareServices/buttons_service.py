"""
Button service for handling input events.
Fake implementation for debugging without hardware.
"""
import asyncio
import sys
from typing import Callable


class ButtonService:
    """Manages button input handling."""
    
    def __init__(self):
        self.on_next_callback = None
        self.on_prev_callback = None
        self.running = False
        self.loop = None
    
    def set_callbacks(self, on_next: Callable = None, on_prev: Callable = None):
        """Set callback functions for button presses."""
        self.on_next_callback = on_next
        self.on_prev_callback = on_prev
    
    async def start_fake_buttons(self):
        """Start fake button listener that responds to keyboard input."""
        self.running = True
        self.loop = asyncio.get_event_loop()
        print("[BUTTONS] Fake button service started")
        
        while self.running:
            await asyncio.sleep(0.1)
    
    def trigger_next(self):
        """Manually trigger next button (for debugging)."""
        if self.on_next_callback:
            if self.loop and self.loop.is_running():
                asyncio.run_coroutine_threadsafe(self._async_next(), self.loop)
            else:
                self.on_next_callback()
    
    def trigger_prev(self):
        """Manually trigger previous button (for debugging)."""
        if self.on_prev_callback:
            if self.loop and self.loop.is_running():
                asyncio.run_coroutine_threadsafe(self._async_prev(), self.loop)
            else:
                self.on_prev_callback()
    
    async def _async_next(self):
        """Async wrapper for next callback."""
        self.on_next_callback()
    
    async def _async_prev(self):
        """Async wrapper for prev callback."""
        self.on_prev_callback()
    
    def stop(self):
        """Stop the button service."""
        self.running = False
