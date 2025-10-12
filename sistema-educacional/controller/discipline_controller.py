from .websocket_manager import WebSocketManager

ws_manager = WebSocketManager()

def listar_disciplinas():
    """Lista todas as disciplinas no sistema"""
    try:
        msg = {"action": "listar_disciplinas"}
        return ws_manager.send_and_receive(msg)
    except Exception as e:
        return {"status": "error", "message": f"Falha de conexão: {e}"}

def cadastrar_disciplina(nome_disciplina: str, curso_id: str = None, professor_id: str = None):
    """Cadastra uma nova disciplina no sistema via WebSocket e opcionalmente associa a um curso e professor"""
    if not nome_disciplina.strip():
        return {
            "status": "error", 
            "message": "Nome da disciplina é obrigatório",
            "clear_form": False
        }

    try:
        msg = {
            "action": "cadastrar_disciplina",
            "nome": nome_disciplina
        }
        resposta = ws_manager.send_and_receive(msg)
        
        if resposta.get("status") == "ok":
            disciplina_id = resposta["data"]["id"]
            
            # Associar ao curso se especificado
            if curso_id:
                msg_curso = {
                    "action": "associar_disciplina_curso",
                    "id_disciplina": disciplina_id,
                    "id_curso": curso_id
                }
                resp_curso = ws_manager.send_and_receive(msg_curso)
                
                if resp_curso.get("status") != "ok":
                    resposta["message"] = f"Disciplina criada, mas houve um erro ao associar ao curso: {resp_curso.get('message')}"
                    return resposta
            
            # Atribuir professor se especificado
            if professor_id:
                msg_prof = {
                    "action": "atribuir_professor_disciplina",
                    "id_disciplina": disciplina_id,
                    "id_professor": professor_id
                }
                resp_prof = ws_manager.send_and_receive(msg_prof)
                
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
        msg = {
            "action": "associar_disciplina_curso",
            "id_disciplina": id_disciplina,
            "id_curso": id_curso
        }
        resposta = ws_manager.send_and_receive(msg)
        
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