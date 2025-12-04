"""
Main entry point for the Muure backend server.
Controls all services and starts the API server.
"""
from server import APIServer
from config_reader import Config
from state_manager import StateManager

class MuureServer:
    """Main Muure backend."""
    
    def __init__(self):
        self.config = Config()
        self.server = APIServer(self.config)

        self.state_manager = StateManager()
    
    def run(self):
        """Start the backend server."""
        print("="*60)
        print("Starting Muure Server")
        print("="*60)
        
        self.server.start()


if __name__ == "__main__":
    backend = MuureServer()
    backend.run()
