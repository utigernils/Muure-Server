"""
Scheduler service for periodic display updates.
"""
import asyncio
from display_controller import DisplayController


class SchedulerService:
    """Manages periodic display refresh scheduling."""
    
    def __init__(self, display_controller: DisplayController, interval_seconds: int = 60):
        self.display_controller = display_controller
        self.interval_seconds = interval_seconds
        self.running = False
        self.task = None
    
    async def start(self):
        """Start the periodic update scheduler."""
        self.running = True
        print(f"[SCHEDULER] Started with {self.interval_seconds}s interval")
        
        await asyncio.sleep(3)
        
        await self.display_controller.update_display(force=True)
        
        while self.running:
            await asyncio.sleep(self.interval_seconds)
            if self.running:
                print(f"\n[SCHEDULER] Periodic update triggered")
                await self.display_controller.update_display()
    
    def stop(self):
        """Stop the scheduler."""
        self.running = False
        print("[SCHEDULER] Stopped")
