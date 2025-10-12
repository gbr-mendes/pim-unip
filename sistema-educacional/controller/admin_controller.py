from .websocket_manager import WebSocketManager

ws_manager = WebSocketManager()

def listar_admins():
    """Lista todos os administradores no sistema"""
    try:
        msg = {"action": "listar_admins"}
        return ws_manager.send_and_receive(msg)
    except Exception as e:
        return {"status": "error", "message": f"Falha de conexão: {e}"}

def cadastrar_admin(nome: str, sobrenome: str, email: str, senha: str, confirme_senha: str):
    """Cadastra um novo administrador no sistema via WebSocket"""
    if not nome.strip() or not sobrenome.strip() or not email.strip():
        return {
            "status": "error", 
            "message": "Nome, sobrenome e email são obrigatórios",
            "clear_form": False
        }

    if senha != confirme_senha:
        return {
            "status": "error", 
            "message": "Senhas não conferem",
            "clear_form": False
        }

    try:
        msg = {
            "action": "cadastrar_admin",
            "nome": nome,
            "sobrenome": sobrenome,
            "email": email,
            "senha": senha
        }
        resposta = ws_manager.send_and_receive(msg)
        
        if resposta.get("status") == "ok":
            resposta["clear_form"] = True
            resposta["message"] = f"Administrador {nome} {sobrenome} cadastrado com sucesso!"
        else:
            resposta["clear_form"] = False
            
        return resposta
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Falha de conexão: {e}",
            "clear_form": False
        }
