from .websocket_manager import WebSocketManager

ws_manager = WebSocketManager()

def listar_modulos():
    """Lista todos os módulos no sistema"""
    try:
        msg = {"action": "listar_modulos"}
        return ws_manager.send_and_receive(msg)
    except Exception as e:
        return {"status": "error", "message": f"Falha de conexão: {e}"}

def listar_modulos_disciplina(disciplina_id):
    """Lista módulos de uma disciplina específica"""
    try:
        msg = {"action": "listar_modulos_disciplina", "disciplina_id": disciplina_id}
        return ws_manager.send_and_receive(msg)
    except Exception as e:
        return {"status": "error", "message": f"Falha de conexão: {e}"}

def criar_modulo(disciplina_id, nome, descricao=""):
    """Cria um novo módulo para uma disciplina"""
    if not nome.strip():
        return {"status": "error", "message": "Nome do módulo é obrigatório"}
    
    try:
        msg = {
            "action": "criar_modulo",
            "disciplina_id": disciplina_id,
            "nome": nome,
            "descricao": descricao
        }
        return ws_manager.send_and_receive(msg)
    except Exception as e:
        return {"status": "error", "message": f"Falha de conexão: {e}"}

def atualizar_modulo(modulo_id, nome, descricao=""):
    """Atualiza um módulo existente"""
    if not nome.strip():
        return {"status": "error", "message": "Nome do módulo é obrigatório"}
    
    try:
        msg = {
            "action": "atualizar_modulo",
            "modulo_id": modulo_id,
            "nome": nome,
            "descricao": descricao
        }
        return ws_manager.send_and_receive(msg)
    except Exception as e:
        return {"status": "error", "message": f"Falha de conexão: {e}"}

def excluir_modulo(modulo_id):
    """Exclui um módulo"""
    try:
        msg = {"action": "excluir_modulo", "modulo_id": modulo_id}
        return ws_manager.send_and_receive(msg)
    except Exception as e:
        return {"status": "error", "message": f"Falha de conexão: {e}"}