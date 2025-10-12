import json
import os
from websocket import create_connection
from dotenv import load_dotenv

load_dotenv()

WEBSOCKET_URL = os.getenv("WEBSOCKET_URL") or "wss://d8603a0fc310.ngrok-free.app"

def listar_cursos():
    """Lista todos os cursos no sistema"""
    try:
        ws = create_connection(WEBSOCKET_URL)
        msg = {"action": "listar_cursos"}
        ws.send(json.dumps(msg))
        resposta = json.loads(ws.recv())
        ws.close()
        return resposta
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
        ws = create_connection(WEBSOCKET_URL)
        msg = {
            "action": "cadastrar_curso",
            "nome": nome_curso
        }
        ws.send(json.dumps(msg))
        resposta = json.loads(ws.recv())
        ws.close()
        
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