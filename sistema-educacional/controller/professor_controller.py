from .websocket_manager import WebSocketManager

ws_manager = WebSocketManager()

def listar_professores():
    """Lista todos os professores no sistema"""
    try:
        msg = {"action": "listar_professores"}
        return ws_manager.send_and_receive(msg)
    except Exception as e:
        return {"status": "error", "message": f"Falha de conexão: {e}"}

def cadastrar_professor(nome: str, sobrenome: str, email: str, senha: str, confirme_senha: str):
    """Cadastra um novo professor no sistema via WebSocket"""
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
            "action": "cadastrar_professor",
            "nome": nome,
            "sobrenome": sobrenome,
            "email": email,
            "senha": senha
        }
        resposta = ws_manager.send_and_receive(msg)
        
        if resposta.get("status") == "ok":
            resposta["clear_form"] = True
            resposta["message"] = f"Professor {nome} {sobrenome} cadastrado com sucesso!"
        else:
            resposta["clear_form"] = False
            
        return resposta
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Falha de conexão: {e}",
            "clear_form": False
        }

def atribuir_professor_disciplina(id_professor: str, id_disciplina: str):
    """Atribui um professor a uma disciplina via WebSocket"""
    if not id_professor.strip() or not id_disciplina.strip():
        return {"status": "error", "message": "Professor e Disciplina são obrigatórios"}

    try:
        msg = {
            "action": "atribuir_professor_disciplina",
            "id_professor": id_professor,
            "id_disciplina": id_disciplina
        }
        resposta = ws_manager.send_and_receive(msg)
        if resposta.get("status") == "ok":
            resposta["message"] = "Professor atribuído à disciplina com sucesso!"
            resposta["clear_form"] = True
        else:
            resposta["clear_form"] = False
        return resposta
    except Exception as e:
        return {"status": "error", "message": f"Falha de conexão: {e}"}