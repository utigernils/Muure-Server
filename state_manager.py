"""
State manager for persisting and managing display state.
"""
import json
from pathlib import Path
from typing import List, Dict, Any


class StateManager:
    """Manages persistent state for the display."""
    
    def __init__(self, state_file: str = "api_state.json"):
        self.state_file = Path(state_file)
        self.pages = [
            {
                "name": "default",
                "left_widgets": [{"widget": "Map", "title": "Location", "icon": "Map"}],
                "right_widgets": [{"widget": "Anniversary", "title": "Anniversary", "icon": "Heart"}]
            },
            {
                "name": "transport",
                "left_widgets": [{"widget": "Transport", "title": "Departures", "icon": "Train"}],
                "right_widgets": [{"widget": "Calendar", "title": "Events", "icon": "Calendar"}]
            },
            {
                "name": "media",
                "left_widgets": [{"widget": "Spotify", "title": "Now Playing", "icon": "Music"}],
                "right_widgets": [{"widget": "Quote", "title": "Quote", "icon": "Quote"}]
            }
        ]
        self.state = self._load_state()
    
    def _load_state(self) -> Dict[str, Any]:
        """Load state from file or create default."""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Failed to load state: {e}, using defaults")
        
        return {
            "current_page_index": 0,
            "last_update": None
        }
    
    def _save_state(self):
        """Persist current state to file."""
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2)
        except Exception as e:
            print(f"Failed to save state: {e}")
    
    def get_current_page(self) -> Dict[str, Any]:
        """Get the currently active page configuration."""
        index = self.state["current_page_index"]
        return self.pages[index]
    
    def next_page(self):
        """Switch to the next page (cycles)."""
        self.state["current_page_index"] = (self.state["current_page_index"] + 1) % len(self.pages)
        self._save_state()
        print(f"Switched to page: {self.get_current_page()['name']}")
    
    def prev_page(self):
        """Switch to the previous page (cycles)."""
        self.state["current_page_index"] = (self.state["current_page_index"] - 1) % len(self.pages)
        self._save_state()
        print(f"Switched to page: {self.get_current_page()['name']}")
    
    def get_page_count(self) -> int:
        """Get total number of pages."""
        return len(self.pages)
    
    def update_timestamp(self, timestamp: str):
        """Update the last update timestamp."""
        self.state["last_update"] = timestamp
        self._save_state()
