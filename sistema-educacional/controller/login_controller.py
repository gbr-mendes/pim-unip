import json
import os
from websocket import create_connection
from dotenv import load_dotenv

load_dotenv()

WEBSOCKET_URL = os.getenv("WEBSOCKET_URL") or "wss://d8603a0fc310.ngrok-free.app"

def tentar_login(username, password):
    """Envia dados ao servidor e recebe resposta de autenticação"""
    try:
        ws = create_connection(WEBSOCKET_URL)
        msg = {"action": "login", "username": username, "password": password}
        ws.send(json.dumps(msg))

        resposta = json.loads(ws.recv())
        ws.close()

        return resposta
    except Exception as e:
        return {"status": "error", "message": f"Falha de conexão: {e}"}
