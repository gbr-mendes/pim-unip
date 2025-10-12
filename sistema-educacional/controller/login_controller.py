from .websocket_manager import WebSocketManager

ws_manager = WebSocketManager()

def tentar_login(username, password):
    """Envia dados ao servidor e recebe resposta de autenticação"""
    try:
        msg = {"action": "login", "username": username, "password": password}
        return ws_manager.send_and_receive(msg)
    except Exception as e:
        return {"status": "error", "message": f"Falha de conexão: {e}"}
