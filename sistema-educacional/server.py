from websocket_server import WebsocketServer
import json
from model.data_access import (
    autenticar_usuario, cadastrar_novo_usuario, cadastrar_novo_curso,
    cadastrar_nova_disciplina, criar_nova_turma, associar_disciplina_curso,
    atribuir_professor_disciplina, associar_turma_curso, atribuir_aluno_turma,
    atribuir_disciplina_turma, carregar_usuarios, carregar_cursos,
    carregar_disciplinas, carregar_turmas, carregar_modulos, carregar_aulas,
    criar_modulo, atualizar_modulo, excluir_modulo, listar_modulos_disciplina,
    criar_aula, atualizar_aula, excluir_aula, listar_aulas_modulo, obter_aula
)

def handle_listar_admins(data):
    usuarios = carregar_usuarios()
    admins = [u for u in usuarios if u.get("role") == "admin"]
    return {
        "status": "ok",
        "data": [{"id": u["id"], "nome": u["nome"], "sobrenome": u["sobrenome"], "email": u["username"]} for u in admins]
    }

def handle_listar_alunos(data):
    usuarios = carregar_usuarios()
    alunos = [u for u in usuarios if u.get("role") == "aluno"]
    return {
        "status": "ok",
        "data": [{"id": u["id"], "nome": u["nome"], "sobrenome": u["sobrenome"], "email": u["username"]} for u in alunos]
    }

def handle_listar_professores(data):
    usuarios = carregar_usuarios()
    professores = [u for u in usuarios if u.get("role") == "professor"]
    return {
        "status": "ok",
        "data": [{"id": u["id"], "nome": u["nome"], "sobrenome": u["sobrenome"], "email": u["username"]} for u in professores]
    }

def handle_listar_cursos(data):
    cursos = carregar_cursos()
    return {
        "status": "ok",
        "data": [{"id": c["id"], "nome": c["nome"], "disciplinas": c["disciplinas"]} for c in cursos]
    }

def handle_listar_disciplinas(data):
    disciplinas = carregar_disciplinas()
    return {
        "status": "ok",
        "data": [{"id": d["id"], "nome": d["nome"], "professor_id": d["professor_id"], "curso_id": d["curso_id"]} for d in disciplinas]
    }

def handle_listar_turmas(data):
    turmas = carregar_turmas()
    return {
        "status": "ok",
        "data": [{"id": t["id"], "nome": t["nome"], "curso_id": t["curso_id"], "alunos": t["alunos"], "disciplinas": t["disciplinas"]} for t in turmas]
    }

def handle_login(data):
    user = data["username"]
    pwd = data["password"]
    
    usuario = autenticar_usuario(user, pwd)
    if usuario:
        return {
            "status": "ok",
            "message": "Login bem-sucedido",
            "user": {
                "id": usuario["id"],
                "username": usuario["username"],
                "nome": usuario["nome"],
                "sobrenome": usuario["sobrenome"],
                "role": usuario["role"]
            }
        }
    return {"status": "error", "message": "Credenciais inválidas"}

def handle_cadastrar_admin(data):
    # Verifica se o usuário atual é um admin
    # if not data.get("current_user") or data["current_user"].get("role") != "admin":
    #     return {"status": "error", "message": "Apenas administradores podem cadastrar outros administradores"}
        
    result = cadastrar_novo_usuario(
        data["nome"], data["sobrenome"], 
        data["email"], data["senha"], "admin"
    )
    if result:
        return {"status": "ok", "message": "Administrador cadastrado com sucesso", "data": result}
    return {"status": "error", "message": "Erro ao cadastrar administrador"}

def handle_cadastrar_aluno(data):
    result = cadastrar_novo_usuario(
        data["nome"], data["sobrenome"], 
        data["email"], data["senha"], "aluno"
    )
    if result:
        return {"status": "ok", "message": "Aluno cadastrado com sucesso", "data": result}
    return {"status": "error", "message": "Erro ao cadastrar aluno"}

def handle_cadastrar_professor(data):
    result = cadastrar_novo_usuario(
        data["nome"], data["sobrenome"], 
        data["email"], data["senha"], "professor"
    )
    if result:
        return {"status": "ok", "message": "Professor cadastrado com sucesso", "data": result}
    return {"status": "error", "message": "Erro ao cadastrar professor"}

def handle_cadastrar_curso(data):
    result = cadastrar_novo_curso(data["nome"])
    if result:
        return {"status": "ok", "message": "Curso cadastrado com sucesso", "data": result}
    return {"status": "error", "message": "Erro ao cadastrar curso"}

def handle_cadastrar_disciplina(data):
    result = cadastrar_nova_disciplina(data["nome"])
    if result:
        return {"status": "ok", "message": "Disciplina cadastrada com sucesso", "data": result}
    return {"status": "error", "message": "Erro ao cadastrar disciplina"}

def handle_criar_turma(data):
    result = criar_nova_turma(data["nome"])
    if result:
        return {"status": "ok", "message": "Turma criada com sucesso", "data": result}
    return {"status": "error", "message": "Erro ao criar turma"}

def handle_associar_disciplina_curso(data):
    result = associar_disciplina_curso(data["id_disciplina"], data["id_curso"])
    if result:
        return {"status": "ok", "message": "Disciplina associada ao curso com sucesso"}
    return {"status": "error", "message": "Erro ao associar disciplina ao curso"}

def handle_atribuir_professor_disciplina(data):
    result = atribuir_professor_disciplina(data["id_professor"], data["id_disciplina"])
    if result:
        return {"status": "ok", "message": "Professor atribuído à disciplina com sucesso"}
    return {"status": "error", "message": "Erro ao atribuir professor à disciplina"}

def handle_associar_turma_curso(data):
    result = associar_turma_curso(data["id_turma"], data["id_curso"])
    if result:
        return {"status": "ok", "message": "Turma associada ao curso com sucesso"}
    return {"status": "error", "message": "Erro ao associar turma ao curso"}

def handle_atribuir_aluno_turma(data):
    result = atribuir_aluno_turma(data["id_aluno"], data["id_turma"])
    if result:
        return {"status": "ok", "message": "Aluno atribuído à turma com sucesso"}
    return {"status": "error", "message": "Erro ao atribuir aluno à turma"}

def handle_associar_disciplina_turma(data):
    result = atribuir_disciplina_turma(data["id_disciplina"], data["id_turma"])
    if result:
        return {"status": "ok", "message": "Disciplina associada à turma com sucesso"}
    return {"status": "error", "message": "Erro ao associar disciplina à turma"}

# Handlers para módulos
def handle_listar_modulos(data):
    modulos = carregar_modulos()
    return {"status": "ok", "data": modulos}

def handle_listar_modulos_disciplina(data):
    modulos = listar_modulos_disciplina(data["disciplina_id"])
    return {"status": "ok", "data": modulos}

def handle_criar_modulo(data):
    modulo = criar_modulo(data["disciplina_id"], data["nome"], data.get("descricao", ""))
    if modulo:
        return {"status": "ok", "data": modulo, "message": "Módulo criado com sucesso"}
    return {"status": "error", "message": "Erro ao criar módulo"}

def handle_atualizar_modulo(data):
    result = atualizar_modulo(data["modulo_id"], data["nome"], data.get("descricao", ""))
    if result:
        return {"status": "ok", "message": "Módulo atualizado com sucesso"}
    return {"status": "error", "message": "Erro ao atualizar módulo"}

def handle_excluir_modulo(data):
    result = excluir_modulo(data["modulo_id"])
    if result:
        return {"status": "ok", "message": "Módulo excluído com sucesso"}
    return {"status": "error", "message": "Erro ao excluir módulo"}

# Handlers para aulas
def handle_listar_aulas(data):
    aulas = carregar_aulas()
    return {"status": "ok", "data": aulas}

def handle_listar_aulas_modulo(data):
    aulas = listar_aulas_modulo(data["modulo_id"])
    return {"status": "ok", "data": aulas}

def handle_criar_aula(data):
    aula = criar_aula(
        data["modulo_id"], 
        data["titulo"], 
        data["resumo"], 
        data.get("video_url", ""),
        data.get("ordem")
    )
    if aula:
        return {"status": "ok", "data": aula, "message": "Aula criada com sucesso"}
    return {"status": "error", "message": "Erro ao criar aula"}

def handle_atualizar_aula(data):
    result = atualizar_aula(
        data["aula_id"], 
        data["titulo"], 
        data["resumo"], 
        data.get("video_url", ""),
        data.get("ordem")
    )
    if result:
        return {"status": "ok", "message": "Aula atualizada com sucesso"}
    return {"status": "error", "message": "Erro ao atualizar aula"}

def handle_excluir_aula(data):
    result = excluir_aula(data["aula_id"])
    if result:
        return {"status": "ok", "message": "Aula excluída com sucesso"}
    return {"status": "error", "message": "Erro ao excluir aula"}

def handle_obter_aula(data):
    aula = obter_aula(data["aula_id"])
    if aula:
        return {"status": "ok", "data": aula}
    return {"status": "error", "message": "Aula não encontrada"}

# Mapeamento de ações para handlers
action_handlers = {
    "login": handle_login,
    "cadastrar_admin": handle_cadastrar_admin,
    "cadastrar_aluno": handle_cadastrar_aluno,
    "cadastrar_professor": handle_cadastrar_professor,
    "cadastrar_curso": handle_cadastrar_curso,
    "cadastrar_disciplina": handle_cadastrar_disciplina,
    "criar_turma": handle_criar_turma,
    "associar_disciplina_curso": handle_associar_disciplina_curso,
    "atribuir_professor_disciplina": handle_atribuir_professor_disciplina,
    "associar_turma_curso": handle_associar_turma_curso,
    "atribuir_aluno_turma": handle_atribuir_aluno_turma,
    "associar_disciplina_turma": handle_associar_disciplina_turma,
    "listar_admins": handle_listar_admins,
    "listar_alunos": handle_listar_alunos,
    "listar_professores": handle_listar_professores,
    "listar_cursos": handle_listar_cursos,
    "listar_disciplinas": handle_listar_disciplinas,
    "listar_turmas": handle_listar_turmas,
    # Módulos
    "listar_modulos": handle_listar_modulos,
    "listar_modulos_disciplina": handle_listar_modulos_disciplina,
    "criar_modulo": handle_criar_modulo,
    "atualizar_modulo": handle_atualizar_modulo,
    "excluir_modulo": handle_excluir_modulo,
    # Aulas
    "listar_aulas": handle_listar_aulas,
    "listar_aulas_modulo": handle_listar_aulas_modulo,
    "criar_aula": handle_criar_aula,
    "atualizar_aula": handle_atualizar_aula,
    "excluir_aula": handle_excluir_aula,
    "obter_aula": handle_obter_aula,
}

def receber_mensagem(client, server, message):
    try:
        data = json.loads(message)
        action = data.get("action")
        
        if action in action_handlers:
            resposta = action_handlers[action](data)
        else:
            resposta = {"status": "error", "message": "Ação não reconhecida"}
            
        server.send_message(client, json.dumps(resposta))
    except Exception as e:
        server.send_message(client, json.dumps({
            "status": "error",
            "message": f"Erro interno do servidor: {str(e)}"
        }))

if __name__ == "__main__":
    server = WebsocketServer(host="0.0.0.0", port=8080)
    server.set_fn_message_received(receber_mensagem)
    print("Servidor rodando na porta 8080...")
    server.run_forever()
