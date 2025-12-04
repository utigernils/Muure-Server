"""
State manager for persisting and managing display state.
"""
import json
from config_reader import Config
from pathlib import Path
from typing import List, Dict, Any


class StateManager:
    """Manages persistent state for the display."""

    def __init__(self, state_file: str = "api_state.json"):
        self.state_file = Path(state_file)
        self.config = Config()

        # All available widgets
        self.widgets = [
            {"widget": "Anniversary", "title": "Jahrestag", "icon": "Heart"},
            {"widget": "Calendar", "title": "Kalender", "icon": "Calendar"},
            {"widget": "CurrentWeather", "title": "Wetter", "icon": "Thermometer"},
            {"widget": "ForecastWeather", "title": "Wettervorhersage", "icon": "CloudSun"},
            {"widget": "Map", "title": f"Wo ist {self.config.my_name}", "icon": "Map"},
            {"widget": "Quote", "title": "Zitat", "icon": "Quote"},
            {"widget": "Spotify", "title": f"Was hört {self.config.my_name}", "icon": "Music"},
            {"widget": "Transport", "title": "Fahrplan", "icon": "RailSymbol"},
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

        # default widget positions
        return {
            "left_widget_index": 0,
            "right_widget_index": 1
        }

    def _save_state(self):
        """Persist current state to file."""
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2)
        except Exception as e:
            print(f"Failed to save state: {e}")

    def get_left_widget(self) -> Dict[str, Any]:
        return self.widgets[self.state["left_widget_index"]]

    def get_right_widget(self) -> Dict[str, Any]:
        return self.widgets[self.state["right_widget_index"]]

    def next_left_widget(self):
        """Cycle the left widget forward."""
        self.state["left_widget_index"] = (self.state["left_widget_index"] + 1) % len(self.widgets)
        self._save_state()
        print(f"Left widget is now: {self.get_left_widget()['widget']}")

    def next_right_widget(self):
        """Cycle the right widget forward."""
        self.state["right_widget_index"] = (self.state["right_widget_index"] + 1) % len(self.widgets)
        self._save_state()
        print(f"Right widget is now: {self.get_right_widget()['widget']}")

    def update_timestamp(self, timestamp: str):
        """Update last update timestamp."""
        self.state["last_update"] = timestamp
        self._save_state()
