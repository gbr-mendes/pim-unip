import json
import os
from websocket import create_connection
from dotenv import load_dotenv

load_dotenv()

WEBSOCKET_URL = os.getenv("WEBSOCKET_URL")

# =====================================================
# === ADMINISTRADORES ================================
# =====================================================

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
        ws = create_connection(WEBSOCKET_URL)
        msg = {
            "action": "cadastrar_admin",
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

# =====================================================
# === ALUNOS ==========================================
# =====================================================

def cadastrar_aluno(nome: str, sobrenome: str, email: str, senha: str, confirme_senha: str):
    """Cadastra um novo aluno no sistema via WebSocket"""
    if not nome.strip() or not sobrenome.strip() or not email.strip():
        return {
            "status": "error", 
            "message": "Nome, sobrenome e email são obrigatórios",
            "clear_form": False  # Não limpa o form em caso de erro de validação
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
        
        if resposta.get("status") == "ok":
            # Adiciona informação para limpar o formulário em caso de sucesso
            resposta["clear_form"] = True
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


# =====================================================
# === PROFESSORES =====================================
# =====================================================

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


# =====================================================
# === CURSOS ==========================================
# =====================================================

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


# =====================================================
# === DISCIPLINAS =====================================
# =====================================================

def cadastrar_disciplina(nome_disciplina: str):
    """Cadastra uma nova disciplina no sistema via WebSocket"""
    if not nome_disciplina.strip():
        return {
            "status": "error", 
            "message": "Nome da disciplina é obrigatório",
            "clear_form": False
        }

    try:
        ws = create_connection(WEBSOCKET_URL)
        msg = {
            "action": "cadastrar_disciplina",
            "nome": nome_disciplina
        }
        ws.send(json.dumps(msg))
        resposta = json.loads(ws.recv())
        ws.close()
        
        if resposta.get("status") == "ok":
            resposta["clear_form"] = True
            resposta["message"] = f"Disciplina '{nome_disciplina}' cadastrada com sucesso!"
        else:
            resposta["clear_form"] = False
            
        return resposta
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Falha de conexão: {e}",
            "clear_form": False
        }


def associar_disciplina_curso(id_disciplina: str, id_curso: str):
    """Associa uma disciplina a um curso via WebSocket"""
    if not id_disciplina.strip() or not id_curso.strip():
        return {
            "status": "error", 
            "message": "Disciplina e Curso são obrigatórios",
            "clear_form": False
        }

    try:
        ws = create_connection(WEBSOCKET_URL)
        msg = {
            "action": "associar_disciplina_curso",
            "id_disciplina": id_disciplina,
            "id_curso": id_curso
        }
        ws.send(json.dumps(msg))
        resposta = json.loads(ws.recv())
        ws.close()
        
        if resposta.get("status") == "ok":
            resposta["clear_form"] = True
            resposta["message"] = "Disciplina associada ao curso com sucesso!"
        else:
            resposta["clear_form"] = False
            
        return resposta
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Falha de conexão: {e}",
            "clear_form": False
        }


# =====================================================
# === PROFESSOR ↔ DISCIPLINA ==========================
# =====================================================

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


# =====================================================
# === TURMAS ==========================================
# =====================================================

def criar_turma(nome_turma: str):
    """Cria uma nova turma no sistema via WebSocket"""
    if not nome_turma.strip():
        return {
            "status": "error", 
            "message": "Nome da turma é obrigatório",
            "clear_form": False
        }

    try:
        ws = create_connection(WEBSOCKET_URL)
        msg = {
            "action": "criar_turma",
            "nome": nome_turma
        }
        ws.send(json.dumps(msg))
        resposta = json.loads(ws.recv())
        ws.close()
        
        if resposta.get("status") == "ok":
            resposta["clear_form"] = True
            resposta["message"] = f"Turma '{nome_turma}' criada com sucesso!"
        else:
            resposta["clear_form"] = False
            
        return resposta
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Falha de conexão: {e}",
            "clear_form": False
        }


def associar_turma_curso(id_turma: str, id_curso: str):
    """Associa uma turma a um curso via WebSocket"""
    if not id_turma.strip() or not id_curso.strip():
        return {
            "status": "error", 
            "message": "Turma e Curso são obrigatórios",
            "clear_form": False
        }

    try:
        ws = create_connection(WEBSOCKET_URL)
        msg = {
            "action": "associar_turma_curso",
            "id_turma": id_turma,
            "id_curso": id_curso
        }
        ws.send(json.dumps(msg))
        resposta = json.loads(ws.recv())
        ws.close()
        
        if resposta.get("status") == "ok":
            resposta["clear_form"] = True
            resposta["message"] = "Turma associada ao curso com sucesso!"
        else:
            resposta["clear_form"] = False
            
        return resposta
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Falha de conexão: {e}",
            "clear_form": False
        }


# =====================================================
# === ATRIBUIÇÕES / RELAÇÕES ==========================
# =====================================================

def atribuir_aluno_turma(id_aluno: str, id_turma: str):
    """Atribui um aluno a uma turma via WebSocket"""
    if not id_aluno.strip() or not id_turma.strip():
        return {
            "status": "error", 
            "message": "Aluno e Turma são obrigatórios",
            "clear_form": False
        }

    try:
        ws = create_connection(WEBSOCKET_URL)
        msg = {
            "action": "atribuir_aluno_turma",
            "id_aluno": id_aluno,
            "id_turma": id_turma
        }
        ws.send(json.dumps(msg))
        resposta = json.loads(ws.recv())
        ws.close()
        
        if resposta.get("status") == "ok":
            resposta["clear_form"] = True
            resposta["message"] = "Aluno atribuído à turma com sucesso!"
        else:
            resposta["clear_form"] = False
            
        return resposta
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Falha de conexão: {e}",
            "clear_form": False
        }


def atribuir_materia_professor(id_materia: str, id_professor: str):
    """Atribui uma matéria a um professor via WebSocket (mantido para compatibilidade)"""
    if not id_materia.strip() or not id_professor.strip():
        return {
            "status": "error", 
            "message": "Matéria e Professor são obrigatórios",
            "clear_form": False
        }

    try:
        ws = create_connection(WEBSOCKET_URL)
        msg = {
            "action": "atribuir_materia_professor",
            "id_materia": id_materia,
            "id_professor": id_professor
        }
        ws.send(json.dumps(msg))
        resposta = json.loads(ws.recv())
        ws.close()
        
        if resposta.get("status") == "ok":
            resposta["clear_form"] = True
            resposta["message"] = "Matéria atribuída ao professor com sucesso!"
        else:
            resposta["clear_form"] = False
            
        return resposta
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Falha de conexão: {e}",
            "clear_form": False
        }


def associar_disciplina_turma(id_disciplina: str, id_turma: str):
    """Associa uma disciplina a uma turma via WebSocket"""
    if not id_disciplina.strip() or not id_turma.strip():
        return {
            "status": "error", 
            "message": "Disciplina e Turma são obrigatórias",
            "clear_form": False
        }

    try:
        ws = create_connection(WEBSOCKET_URL)
        msg = {
            "action": "associar_disciplina_turma",
            "id_disciplina": id_disciplina,
            "id_turma": id_turma
        }
        ws.send(json.dumps(msg))
        resposta = json.loads(ws.recv())
        ws.close()
        
        if resposta.get("status") == "ok":
            resposta["clear_form"] = True
            resposta["message"] = "Disciplina associada à turma com sucesso!"
        else:
            resposta["clear_form"] = False
            
        return resposta
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Falha de conexão: {e}",
            "clear_form": False
        }
