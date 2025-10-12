import json
import os
from websocket import create_connection
from dotenv import load_dotenv

load_dotenv()

WEBSOCKET_URL = os.getenv("WEBSOCKET_URL") or "wss://d8603a0fc310.ngrok-free.app"

def listar_professores():
    """Lista todos os professores no sistema"""
    try:
        ws = create_connection(WEBSOCKET_URL)
        msg = {"action": "listar_professores"}
        ws.send(json.dumps(msg))
        resposta = json.loads(ws.recv())
        ws.close()
        return resposta
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
        ws = create_connection(WEBSOCKET_URL)
        msg = {
            "action": "cadastrar_professor",
            "nome": nome,
            "sobrenome": sobrenome,
            "email": email,
            "senha": senha
        }
        ws.send(json.dumps(msg))
        resposta = json.loads(ws.recv())
        ws.close()
        
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
        ws = create_connection(WEBSOCKET_URL)
        msg = {
            "action": "atribuir_professor_disciplina",
            "id_professor": id_professor,
            "id_disciplina": id_disciplina
        }
        ws.send(json.dumps(msg))
        resposta = json.loads(ws.recv())
        ws.close()
        if resposta.get("status") == "ok":
            resposta["message"] = "Professor atribuído à disciplina com sucesso!"
            resposta["clear_form"] = True
        else:
            resposta["clear_form"] = False
        return resposta
    except Exception as e:
        return {"status": "error", "message": f"Falha de conexão: {e}"}