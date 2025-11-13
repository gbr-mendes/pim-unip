from .websocket_manager import WebSocketManager

ws_manager = WebSocketManager()

def listar_aulas():
    """Lista todas as aulas no sistema"""
    try:
        msg = {"action": "listar_aulas"}
        return ws_manager.send_and_receive(msg)
    except Exception as e:
        return {"status": "error", "message": f"Falha de conexão: {e}"}

def listar_aulas_modulo(modulo_id):
    """Lista aulas de um módulo específico"""
    try:
        msg = {"action": "listar_aulas_modulo", "modulo_id": modulo_id}
        return ws_manager.send_and_receive(msg)
    except Exception as e:
        return {"status": "error", "message": f"Falha de conexão: {e}"}

def criar_aula(modulo_id, titulo, resumo, video_url="", ordem=None):
    """Cria uma nova aula para um módulo"""
    if not titulo.strip():
        return {"status": "error", "message": "Título da aula é obrigatório"}
    
    if not video_url.strip():
        return {"status": "error", "message": "URL do vídeo é obrigatória"}
    
    # Validação básica de URL de vídeo
    import re
    video_patterns = [
        r'youtube\.com/watch\?v=',
        r'youtu\.be/',
        r'vimeo\.com/',
        r'dailymotion\.com/',
    ]
    
    if not any(re.search(pattern, video_url, re.IGNORECASE) for pattern in video_patterns):
        return {"status": "error", "message": "URL do vídeo deve ser do YouTube, Vimeo ou Dailymotion"}
    
    try:
        msg = {
            "action": "criar_aula",
            "modulo_id": modulo_id,
            "titulo": titulo,
            "resumo": resumo,
            "video_url": video_url,
            "ordem": ordem
        }
        return ws_manager.send_and_receive(msg)
    except Exception as e:
        return {"status": "error", "message": f"Falha de conexão: {e}"}

def atualizar_aula(aula_id, titulo, resumo, video_url="", ordem=None):
    """Atualiza uma aula existente"""
    if not titulo.strip():
        return {"status": "error", "message": "Título da aula é obrigatório"}
    
    if not video_url.strip():
        return {"status": "error", "message": "URL do vídeo é obrigatória"}
    
    # Validação básica de URL de vídeo
    import re
    video_patterns = [
        r'youtube\.com/watch\?v=',
        r'youtu\.be/',
        r'vimeo\.com/',
        r'dailymotion\.com/',
    ]
    
    if not any(re.search(pattern, video_url, re.IGNORECASE) for pattern in video_patterns):
        return {"status": "error", "message": "URL do vídeo deve ser do YouTube, Vimeo ou Dailymotion"}
    
    try:
        msg = {
            "action": "atualizar_aula",
            "aula_id": aula_id,
            "titulo": titulo,
            "resumo": resumo,
            "video_url": video_url,
            "ordem": ordem
        }
        return ws_manager.send_and_receive(msg)
    except Exception as e:
        return {"status": "error", "message": f"Falha de conexão: {e}"}

def excluir_aula(aula_id):
    """Exclui uma aula"""
    try:
        msg = {"action": "excluir_aula", "aula_id": aula_id}
        return ws_manager.send_and_receive(msg)
    except Exception as e:
        return {"status": "error", "message": f"Falha de conexão: {e}"}

def obter_aula(aula_id):
    """Obtém detalhes de uma aula específica"""
    try:
        msg = {"action": "obter_aula", "aula_id": aula_id}
        return ws_manager.send_and_receive(msg)
    except Exception as e:
        return {"status": "error", "message": f"Falha de conexão: {e}"}