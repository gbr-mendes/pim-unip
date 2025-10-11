# session.py
_usuario_logado = None

def set_usuario(usuario: dict):
    global _usuario_logado
    _usuario_logado = usuario

def get_usuario() -> dict:
    return _usuario_logado

def limpar_usuario():
    global _usuario_logado
    _usuario_logado = None
