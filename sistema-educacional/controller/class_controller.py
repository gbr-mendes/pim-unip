from .websocket_manager import WebSocketManager

ws_manager = WebSocketManager()

def listar_turmas():
    """Lista todas as turmas no sistema"""
    try:
        msg = {"action": "listar_turmas"}
        return ws_manager.send_and_receive(msg)
    except Exception as e:
        return {"status": "error", "message": f"Falha de conexão: {e}"}

def criar_turma(nome_turma: str, curso_id: str = None, disciplinas_ids: list = None):
    """Cria uma nova turma no sistema via WebSocket e opcionalmente associa a um curso e disciplinas"""
    if not nome_turma.strip():
        return {
            "status": "error", 
            "message": "Nome da turma é obrigatório",
            "clear_form": False
        }

    try:
        msg = {
            "action": "criar_turma",
            "nome": nome_turma
        }
        resposta = ws_manager.send_and_receive(msg)
        
        if resposta.get("status") == "ok":
            turma_id = resposta["data"]["id"]
            success_messages = []
            error_messages = []

            # Se o cadastro foi bem sucedido e um curso foi especificado,
            # associa a turma ao curso
            if curso_id:
                msg_curso = {
                    "action": "associar_turma_curso",
                    "id_turma": turma_id,
                    "id_curso": curso_id
                }
                resp_curso = ws_manager.send_and_receive(msg_curso)
                
                if resp_curso.get("status") == "ok":
                    success_messages.append("associada ao curso")
                else:
                    error_messages.append(f"erro ao associar ao curso: {resp_curso.get('message')}")

            # Se disciplinas foram especificadas, associa cada uma à turma
            if disciplinas_ids:
                for disc_id in disciplinas_ids:
                    msg_disc = {
                        "action": "associar_disciplina_turma",
                        "id_disciplina": disc_id,
                        "id_turma": turma_id
                    }
                    resp_disc = ws_manager.send_and_receive(msg_disc)
                    
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
        msg = {
            "action": "associar_turma_curso",
            "id_turma": id_turma,
            "id_curso": id_curso
        }
        resposta = ws_manager.send_and_receive(msg)
        
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

def atribuir_aluno_turma(id_aluno: str, id_turma: str):
    """Atribui um aluno a uma turma via WebSocket"""
    if not id_aluno.strip() or not id_turma.strip():
        return {
            "status": "error", 
            "message": "Aluno e Turma são obrigatórios",
            "clear_form": False
        }

    try:
        msg = {
            "action": "atribuir_aluno_turma",
            "id_aluno": id_aluno,
            "id_turma": id_turma
        }
        resposta = ws_manager.send_and_receive(msg)
        
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

def associar_disciplina_turma(id_disciplina: str, id_turma: str):
    """Associa uma disciplina a uma turma via WebSocket"""
    if not id_disciplina.strip() or not id_turma.strip():
        return {
            "status": "error", 
            "message": "Disciplina e Turma são obrigatórias",
            "clear_form": False
        }

    try:
        msg = {
            "action": "associar_disciplina_turma",
            "id_disciplina": id_disciplina,
            "id_turma": id_turma
        }
        resposta = ws_manager.send_and_receive(msg)
        
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