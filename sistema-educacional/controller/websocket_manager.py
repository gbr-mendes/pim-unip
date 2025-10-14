import json
import os
from websocket import create_connection
from dotenv import load_dotenv
from threading import Lock

load_dotenv()

class WebSocketManager:
    _instance = None
    _lock = Lock()
    _ws = None
    
    WEBSOCKET_URL = os.getenv("WEBSOCKET_URL") or "wss://c85c0b74a2be.ngrok-free.app"
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(WebSocketManager, cls).__new__(cls)
            return cls._instance
    
    def __init__(self):
        # Initialize only once
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._connect()
    
    def _connect(self):
        """Establish WebSocket connection"""
        try:
            if not self._ws:
                self._ws = create_connection(self.WEBSOCKET_URL)
        except Exception as e:
            print(f"Failed to connect to WebSocket: {e}")
            self._ws = None

    def send_and_receive(self, message):
        """Send a message and receive response, reconnecting if necessary"""
        try:
            if not self._ws:
                self._connect()
            
            if not self._ws:
                return {"status": "error", "message": "Could not establish connection"}
                
            self._ws.send(json.dumps(message))
            return json.loads(self._ws.recv())
        except Exception as e:
            # If there's an error, try to reconnect once
            try:
                self._ws = None
                self._connect()
                if self._ws:
                    self._ws.send(json.dumps(message))
                    return json.loads(self._ws.recv())
            except Exception as reconnect_error:
                return {"status": "error", "message": f"Connection failed: {str(reconnect_error)}"}
            return {"status": "error", "message": f"Connection failed: {str(e)}"}

    def close(self):
        """Close the WebSocket connection"""
        if self._ws:
            try:
                self._ws.close()
            except:
                pass
            finally:
                self._ws = None