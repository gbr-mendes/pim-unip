import json
from websocket import create_connection

def tentar_login(username, password):
    """Envia dados ao servidor e recebe resposta de autenticação"""
    try:
        ws = create_connection("ws://localhost:8080")
        msg = {"action": "login", "username": username, "password": password}
        ws.send(json.dumps(msg))

        resposta = json.loads(ws.recv())
        ws.close()

        return resposta
    except Exception as e:
        return {"status": "error", "message": f"Falha de conexão: {e}"}
