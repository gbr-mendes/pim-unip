"""
Controller para funcionalidades específicas do aluno
"""
from controller.websocket_manager import WebSocketManager

# Instância única do WebSocket Manager
ws_manager = WebSocketManager()

def listar_disciplinas_aluno(aluno_id):
    """Lista as disciplinas em que o aluno está matriculado"""
    try:
        msg = {"action": "listar_disciplinas_aluno", "aluno_id": aluno_id}
        resposta = ws_manager.send_and_receive(msg)
        return resposta
    except Exception as e:
        return {"status": "error", "message": f"Erro de comunicação: {str(e)}"}

def obter_progresso_aluno(aluno_id, disciplina_id=None):
    """Obtém o progresso do aluno em uma disciplina específica ou todas"""
    try:
        msg = {"action": "obter_progresso_aluno", "aluno_id": aluno_id}
        if disciplina_id:
            msg["disciplina_id"] = disciplina_id
        resposta = ws_manager.send_and_receive(msg)
        return resposta
    except Exception as e:
        return {"status": "error", "message": f"Erro de comunicação: {str(e)}"}

def marcar_aula_concluida(aluno_id, aula_id):
    """Marca uma aula como concluída pelo aluno"""
    try:
        msg = {
            "action": "marcar_aula_concluida", 
            "aluno_id": aluno_id,
            "aula_id": aula_id
        }
        resposta = ws_manager.send_and_receive(msg)
        return resposta
    except Exception as e:
        return {"status": "error", "message": f"Erro de comunicação: {str(e)}"}

def obter_estatisticas_aluno(aluno_id):
    """Obtém estatísticas gerais de progresso do aluno"""
    try:
        msg = {"action": "obter_estatisticas_aluno", "aluno_id": aluno_id}
        resposta = ws_manager.send_and_receive(msg)
        return resposta
    except Exception as e:
        return {"status": "error", "message": f"Erro de comunicação: {str(e)}"}

def buscar_conteudo_aluno(aluno_id, termo_busca):
    """Busca conteúdo nas disciplinas do aluno"""
    try:
        msg = {
            "action": "buscar_conteudo_aluno",
            "aluno_id": aluno_id,
            "termo_busca": termo_busca
        }
        resposta = ws_manager.send_and_receive(msg)
        return resposta
    except Exception as e:
        return {"status": "error", "message": f"Erro de comunicação: {str(e)}"}

def listar_modulos_disciplina_aluno(disciplina_id):
    """Lista os módulos de uma disciplina"""
    try:
        msg = {"action": "listar_modulos_disciplina", "disciplina_id": disciplina_id}
        resposta = ws_manager.send_and_receive(msg)
        return resposta
    except Exception as e:
        return {"status": "error", "message": f"Erro de comunicação: {str(e)}"}

def listar_aulas_modulo_aluno(modulo_id):
    """Lista as aulas de um módulo"""
    try:
        msg = {"action": "listar_aulas_modulo", "modulo_id": modulo_id}
        resposta = ws_manager.send_and_receive(msg)
        return resposta
    except Exception as e:
        return {"status": "error", "message": f"Erro de comunicação: {str(e)}"}

def obter_aula_aluno(aula_id):
    """Obtém uma aula específica"""
    try:
        msg = {"action": "obter_aula", "aula_id": aula_id}
        resposta = ws_manager.send_and_receive(msg)
        return resposta
    except Exception as e:
        return {"status": "error", "message": f"Erro de comunicação: {str(e)}"}