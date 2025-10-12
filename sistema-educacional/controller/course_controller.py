from .websocket_manager import WebSocketManager

ws_manager = WebSocketManager()

def listar_cursos():
    """Lista todos os cursos no sistema"""
    try:
        msg = {"action": "listar_cursos"}
        return ws_manager.send_and_receive(msg)
    except Exception as e:
        return {"status": "error", "message": f"Falha de conexão: {e}"}

def cadastrar_curso(nome_curso: str):
    """Cadastra um novo curso no sistema via WebSocket"""
    if not nome_curso.strip():
        return {
            "status": "error", 
            "message": "Nome do curso é obrigatório",
            "clear_form": False
        }

    try:
        msg = {
            "action": "cadastrar_curso",
            "nome": nome_curso
        }
        resposta = ws_manager.send_and_receive(msg)
        
        if resposta.get("status") == "ok":
            resposta["clear_form"] = True
            resposta["message"] = f"Curso '{nome_curso}' cadastrado com sucesso!"
        else:
            resposta["clear_form"] = False
            
        return resposta
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Falha de conexão: {e}",
            "clear_form": False
        }