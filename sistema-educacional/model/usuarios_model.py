import json, os
from ctypes import CDLL, c_char_p

# Carregando biblioteca C++
dll_path = os.path.abspath("./cpp_modules/libusuarios.dll")
lib = CDLL(dll_path)

lib.carregar_usuarios_json.argtypes = [c_char_p]
lib.carregar_usuarios_json.restype = c_char_p

USUARIOS_FILE = b"data/usuarios.json"  # bytes para ctypes

def carregar_usuarios():
    # Chama função C++ e converte para Python
    conteudo = lib.carregar_usuarios_json(USUARIOS_FILE)
    usuarios = json.loads(conteudo.decode("utf-8"))
    return usuarios

def autenticar_usuario(username, password):
    usuarios = carregar_usuarios()
    for u in usuarios:
        if u["username"] == username and u["password"] == password:
            return True
    return False
