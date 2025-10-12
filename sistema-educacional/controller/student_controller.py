import json
import os
from websocket import create_connection
from dotenv import load_dotenv

load_dotenv()

WEBSOCKET_URL = os.getenv("WEBSOCKET_URL") or "wss://d8603a0fc310.ngrok-free.app"

def listar_alunos():
    """Lista todos os alunos no sistema"""
    try:
        ws = create_connection(WEBSOCKET_URL)
        msg = {"action": "listar_alunos"}
        ws.send(json.dumps(msg))
        resposta = json.loads(ws.recv())
        ws.close()
        return resposta
    except Exception as e:
        return {"status": "error", "message": f"Falha de conexão: {e}"}

def cadastrar_aluno(nome: str, sobrenome: str, email: str, senha: str, confirme_senha: str, curso_id: str = None, turma_id: str = None):
    """Cadastra um novo aluno no sistema via WebSocket e opcionalmente associa a uma turma"""
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
            "action": "cadastrar_aluno",
            "nome": nome,
            "sobrenome": sobrenome,
            "email": email,
            "senha": senha
        }
        ws.send(json.dumps(msg))
        resposta = json.loads(ws.recv())
        ws.close()
        
        if resposta.get("status") == "ok" and turma_id:
            # Se o cadastro foi bem sucedido e uma turma foi especificada,
            # associa o aluno à turma
            ws = create_connection(WEBSOCKET_URL)
            msg_atrib = {
                "action": "atribuir_aluno_turma",
                "id_aluno": resposta["data"]["id"],
                "id_turma": turma_id
            }
            ws.send(json.dumps(msg_atrib))
            resp_atrib = json.loads(ws.recv())
            ws.close()
            
            if resp_atrib.get("status") == "ok":
                resposta["message"] = f"Aluno {nome} {sobrenome} cadastrado e atribuído à turma com sucesso!"
            else:
                resposta["message"] = f"Aluno cadastrado, mas houve um erro ao atribuir à turma: {resp_atrib.get('message')}"
        
        if resposta.get("status") == "ok":
            resposta["clear_form"] = True
            if not resposta.get("message"):
                resposta["message"] = f"Aluno {nome} {sobrenome} cadastrado com sucesso!"
        else:
            resposta["clear_form"] = False
        
        return resposta
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Falha de conexão: {e}",
            "clear_form": False
        }