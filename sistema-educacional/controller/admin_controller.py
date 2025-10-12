import json
import os
from websocket import create_connection
from dotenv import load_dotenv

load_dotenv()

WEBSOCKET_URL = os.getenv("WEBSOCKET_URL") or "wss://d8603a0fc310.ngrok-free.app"

# =====================================================
# === LISTAR ENTIDADES ===============================
# =====================================================

def listar_admins():
    """Lista todos os administradores no sistema"""
    try:
        ws = create_connection(WEBSOCKET_URL)
        msg = {"action": "listar_admins"}
        ws.send(json.dumps(msg))
        resposta = json.loads(ws.recv())
        ws.close()
        return resposta
    except Exception as e:
        return {"status": "error", "message": f"Falha de conexão: {e}"}

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

def listar_disciplinas():
    """Lista todas as disciplinas no sistema"""
    try:
        ws = create_connection(WEBSOCKET_URL)
        msg = {"action": "listar_disciplinas"}
        ws.send(json.dumps(msg))
        resposta = json.loads(ws.recv())
        ws.close()
        return resposta
    except Exception as e:
        return {"status": "error", "message": f"Falha de conexão: {e}"}

def listar_turmas():
    """Lista todas as turmas no sistema"""
    try:
        ws = create_connection(WEBSOCKET_URL)
        msg = {"action": "listar_turmas"}
        ws.send(json.dumps(msg))
        resposta = json.loads(ws.recv())
        ws.close()
        return resposta
    except Exception as e:
        return {"status": "error", "message": f"Falha de conexão: {e}"}

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

def cadastrar_disciplina(nome_disciplina: str, curso_id: str = None, professor_id: str = None):
    """Cadastra uma nova disciplina no sistema via WebSocket e opcionalmente associa a um curso e professor"""
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
            disciplina_id = resposta["data"]["id"]
            
            # Associar ao curso se especificado
            if curso_id:
                ws = create_connection(WEBSOCKET_URL)
                msg_curso = {
                    "action": "associar_disciplina_curso",
                    "id_disciplina": disciplina_id,
                    "id_curso": curso_id
                }
                ws.send(json.dumps(msg_curso))
                resp_curso = json.loads(ws.recv())
                ws.close()
                
                if resp_curso.get("status") != "ok":
                    resposta["message"] = f"Disciplina criada, mas houve um erro ao associar ao curso: {resp_curso.get('message')}"
                    return resposta
            
            # Atribuir professor se especificado
            if professor_id:
                ws = create_connection(WEBSOCKET_URL)
                msg_prof = {
                    "action": "atribuir_professor_disciplina",
                    "id_disciplina": disciplina_id,
                    "id_professor": professor_id
                }
                ws.send(json.dumps(msg_prof))
                resp_prof = json.loads(ws.recv())
                ws.close()
                
                if resp_prof.get("status") != "ok":
                    resposta["message"] = f"Disciplina criada e associada ao curso, mas houve um erro ao atribuir o professor: {resp_prof.get('message')}"
                    return resposta
            
            resposta["clear_form"] = True
            if not resposta.get("message"):
                resposta["message"] = f"Disciplina '{nome_disciplina}' cadastrada com sucesso!"
                if curso_id and professor_id:
                    resposta["message"] = f"Disciplina '{nome_disciplina}' cadastrada, associada ao curso e professor com sucesso!"
                elif curso_id:
                    resposta["message"] = f"Disciplina '{nome_disciplina}' cadastrada e associada ao curso com sucesso!"
                elif professor_id:
                    resposta["message"] = f"Disciplina '{nome_disciplina}' cadastrada e atribuída ao professor com sucesso!"
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

def criar_turma(nome_turma: str, curso_id: str = None, disciplinas_ids: list = None):
    """Cria uma nova turma no sistema via WebSocket e opcionalmente associa a um curso e disciplinas"""
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
            turma_id = resposta["data"]["id"]
            success_messages = []
            error_messages = []

            # Se o cadastro foi bem sucedido e um curso foi especificado,
            # associa a turma ao curso
            if curso_id:
                ws = create_connection(WEBSOCKET_URL)
                msg_curso = {
                    "action": "associar_turma_curso",
                    "id_turma": turma_id,
                    "id_curso": curso_id
                }
                ws.send(json.dumps(msg_curso))
                resp_curso = json.loads(ws.recv())
                ws.close()
                
                if resp_curso.get("status") == "ok":
                    success_messages.append("associada ao curso")
                else:
                    error_messages.append(f"erro ao associar ao curso: {resp_curso.get('message')}")

            # Se disciplinas foram especificadas, associa cada uma à turma
            if disciplinas_ids:
                for disc_id in disciplinas_ids:
                    ws = create_connection(WEBSOCKET_URL)
                    msg_disc = {
                        "action": "associar_disciplina_turma",
                        "id_disciplina": disc_id,
                        "id_turma": turma_id
                    }
                    ws.send(json.dumps(msg_disc))
                    resp_disc = json.loads(ws.recv())
                    ws.close()
                    
                    if resp_disc.get("status") == "ok":
                        continue
                    else:
                        error_messages.append(f"erro ao associar disciplina {disc_id}: {resp_disc.get('message')}")
                
                if not error_messages:
                    success_messages.append("disciplinas associadas")
            
            # Compõe a mensagem de resposta
            resposta["clear_form"] = True
            base_msg = f"Turma '{nome_turma}' criada"
            if success_messages:
                base_msg += " e " + " e ".join(success_messages)
            base_msg += " com sucesso!"
            
            if error_messages:
                base_msg += " Porém houve alguns erros: " + "; ".join(error_messages)
            
            resposta["message"] = base_msg
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
