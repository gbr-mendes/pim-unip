import json, os, random
from ctypes import CDLL, c_char_p, c_bool

# Carregando biblioteca C++
dll_path = os.path.abspath("./cpp_modules/libdata_access.dll")
lib = CDLL(dll_path)

# Configurando tipos para funções de carregar
for func in ['carregar_usuarios_json', 'carregar_cursos_json', 
            'carregar_disciplinas_json', 'carregar_turmas_json']:
    getattr(lib, func).argtypes = [c_char_p]
    getattr(lib, func).restype = c_char_p

# Configurando tipos para funções de salvar
for func in ['salvar_usuarios_json', 'salvar_cursos_json', 
            'salvar_disciplinas_json', 'salvar_turmas_json']:
    getattr(lib, func).argtypes = [c_char_p, c_char_p]
    getattr(lib, func).restype = c_bool

# Caminhos dos arquivos
DATA_DIR = "data"
USUARIOS_FILE = os.path.join(DATA_DIR, "usuarios.json").encode()
CURSOS_FILE = os.path.join(DATA_DIR, "cursos.json").encode()
DISCIPLINAS_FILE = os.path.join(DATA_DIR, "disciplinas.json").encode()
TURMAS_FILE = os.path.join(DATA_DIR, "turmas.json").encode()

def gerar_id():
    return str(random.randint(1000, 9999))

# Funções de carregamento
def carregar_dados(arquivo, funcao):
    conteudo = funcao(arquivo)
    return json.loads(conteudo.decode("utf-8"))

def salvar_dados(arquivo, dados, funcao):
    conteudo = json.dumps(dados, indent=2).encode()
    return funcao(arquivo, conteudo)

# Funções específicas
def carregar_usuarios():
    return carregar_dados(USUARIOS_FILE, lib.carregar_usuarios_json)

def carregar_cursos():
    return carregar_dados(CURSOS_FILE, lib.carregar_cursos_json)

def carregar_disciplinas():
    return carregar_dados(DISCIPLINAS_FILE, lib.carregar_disciplinas_json)

def carregar_turmas():
    return carregar_dados(TURMAS_FILE, lib.carregar_turmas_json)

def salvar_usuarios(dados):
    return salvar_dados(USUARIOS_FILE, dados, lib.salvar_usuarios_json)

def salvar_cursos(dados):
    return salvar_dados(CURSOS_FILE, dados, lib.salvar_cursos_json)

def salvar_disciplinas(dados):
    return salvar_dados(DISCIPLINAS_FILE, dados, lib.salvar_disciplinas_json)

def salvar_turmas(dados):
    return salvar_dados(TURMAS_FILE, dados, lib.salvar_turmas_json)

# Funções de autenticação
def autenticar_usuario(username, password):
    usuarios = carregar_usuarios()
    for u in usuarios:
        if u["username"] == username and u["password"] == password:
            return {
                "username": u["username"],
                "role": u.get("role", "user"),
                "id": u.get("id", ""),
                "nome": u.get("nome", ""),
                "sobrenome": u.get("sobrenome", "")
            }
    return None

def verificar_admin_existente():
    """Verifica se já existe algum administrador cadastrado"""
    usuarios = carregar_usuarios()
    return any(u.get("role") == "admin" for u in usuarios)

def verificar_permissao_admin(user_id):
    """Verifica se um usuário tem permissões de administrador"""
    if not user_id:
        return False
    usuarios = carregar_usuarios()
    usuario = next((u for u in usuarios if u.get("id") == user_id), None)
    return usuario and usuario.get("role") == "admin"

# Funções administrativas
def cadastrar_novo_usuario(nome, sobrenome, email, senha, role="aluno"):
    usuarios = carregar_usuarios()
    novo_usuario = {
        "username": email,
        "password": senha,
        "nome": nome,
        "sobrenome": sobrenome,
        "role": role,
        "id": gerar_id()
    }
    usuarios.append(novo_usuario)
    if salvar_usuarios(usuarios):
        return {"id": novo_usuario["id"], "username": novo_usuario["username"]}
    return None

def cadastrar_novo_curso(nome):
    cursos = carregar_cursos()
    novo_curso = {
        "id": gerar_id(),
        "nome": nome,
        "disciplinas": []
    }
    cursos.append(novo_curso)
    if salvar_cursos(cursos):
        return novo_curso
    return None

def cadastrar_nova_disciplina(nome):
    disciplinas = carregar_disciplinas()
    nova_disciplina = {
        "id": gerar_id(),
        "nome": nome,
        "professor_id": None,
        "curso_id": None
    }
    disciplinas.append(nova_disciplina)
    if salvar_disciplinas(disciplinas):
        return nova_disciplina
    return None

def criar_nova_turma(nome):
    turmas = carregar_turmas()
    nova_turma = {
        "id": gerar_id(),
        "nome": nome,
        "curso_id": None,
        "alunos": [],
        "disciplinas": []
    }
    turmas.append(nova_turma)
    if salvar_turmas(turmas):
        return nova_turma
    return None

# Funções de associação
def associar_disciplina_curso(id_disciplina, id_curso):
    disciplinas = carregar_disciplinas()
    cursos = carregar_cursos()
    
    disciplina = next((d for d in disciplinas if d["id"] == id_disciplina), None)
    curso = next((c for c in cursos if c["id"] == id_curso), None)
    
    if disciplina and curso:
        disciplina["curso_id"] = id_curso
        if id_disciplina not in curso["disciplinas"]:
            curso["disciplinas"].append(id_disciplina)
        
        if salvar_disciplinas(disciplinas) and salvar_cursos(cursos):
            return True
    return False

def atribuir_professor_disciplina(id_professor, id_disciplina):
    disciplinas = carregar_disciplinas()
    usuarios = carregar_usuarios()
    
    disciplina = next((d for d in disciplinas if d["id"] == id_disciplina), None)
    professor = next((u for u in usuarios if u["id"] == id_professor and u["role"] == "professor"), None)
    
    if disciplina and professor:
        disciplina["professor_id"] = id_professor
        return salvar_disciplinas(disciplinas)
    return False

def associar_turma_curso(id_turma, id_curso):
    turmas = carregar_turmas()
    cursos = carregar_cursos()
    
    turma = next((t for t in turmas if t["id"] == id_turma), None)
    curso = next((c for c in cursos if c["id"] == id_curso), None)
    
    if turma and curso:
        turma["curso_id"] = id_curso
        return salvar_turmas(turmas)
    return False

def atribuir_aluno_turma(id_aluno, id_turma):
    turmas = carregar_turmas()
    usuarios = carregar_usuarios()
    
    turma = next((t for t in turmas if t["id"] == id_turma), None)
    aluno = next((u for u in usuarios if u["id"] == id_aluno and u["role"] == "aluno"), None)
    
    if turma and aluno and id_aluno not in turma["alunos"]:
        turma["alunos"].append(id_aluno)
        return salvar_turmas(turmas)
    return False

def atribuir_disciplina_turma(id_disciplina, id_turma):
    turmas = carregar_turmas()
    disciplinas = carregar_disciplinas()
    
    turma = next((t for t in turmas if t["id"] == id_turma), None)
    disciplina = next((d for d in disciplinas if d["id"] == id_disciplina), None)
    
    if turma and disciplina and id_disciplina not in turma["disciplinas"]:
        turma["disciplinas"].append(id_disciplina)
        return salvar_turmas(turmas)
    return False

# Funções para módulos
MODULOS_FILE = os.path.join(DATA_DIR, "modulos.json").encode()

def carregar_modulos():
    """Carrega módulos do arquivo JSON"""
    try:
        with open("data/modulos.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def salvar_modulos(modulos):
    """Salva módulos no arquivo JSON"""
    try:
        with open("data/modulos.json", "w", encoding="utf-8") as f:
            json.dump(modulos, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False

def criar_modulo(disciplina_id, nome, descricao=""):
    """Cria um novo módulo"""
    modulos = carregar_modulos()
    
    novo_modulo = {
        "id": gerar_id(),
        "disciplina_id": disciplina_id,
        "nome": nome,
        "descricao": descricao,
        "ordem": len([m for m in modulos if m["disciplina_id"] == disciplina_id]) + 1
    }
    
    modulos.append(novo_modulo)
    
    if salvar_modulos(modulos):
        return novo_modulo
    return None

def atualizar_modulo(modulo_id, nome, descricao=""):
    """Atualiza um módulo existente"""
    modulos = carregar_modulos()
    
    for modulo in modulos:
        if modulo["id"] == modulo_id:
            modulo["nome"] = nome
            modulo["descricao"] = descricao
            return salvar_modulos(modulos)
    
    return False

def excluir_modulo(modulo_id):
    """Exclui um módulo e suas aulas"""
    modulos = carregar_modulos()
    aulas = carregar_aulas()
    
    # Remove o módulo
    modulos = [m for m in modulos if m["id"] != modulo_id]
    
    # Remove aulas do módulo
    aulas = [a for a in aulas if a["modulo_id"] != modulo_id]
    
    return salvar_modulos(modulos) and salvar_aulas(aulas)

def listar_modulos_disciplina(disciplina_id):
    """Lista módulos de uma disciplina"""
    modulos = carregar_modulos()
    return [m for m in modulos if m["disciplina_id"] == disciplina_id]

# Funções para aulas
AULAS_FILE = os.path.join(DATA_DIR, "aulas.json").encode()

def carregar_aulas():
    """Carrega aulas do arquivo JSON"""
    try:
        with open("data/aulas.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def salvar_aulas(aulas):
    """Salva aulas no arquivo JSON"""
    try:
        with open("data/aulas.json", "w", encoding="utf-8") as f:
            json.dump(aulas, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False

def criar_aula(modulo_id, titulo, resumo, video_url="", ordem=None):
    """Cria uma nova aula"""
    aulas = carregar_aulas()
    
    if ordem is None:
        ordem = len([a for a in aulas if a["modulo_id"] == modulo_id]) + 1
    
    nova_aula = {
        "id": gerar_id(),
        "modulo_id": modulo_id,
        "titulo": titulo,
        "resumo": resumo,
        "video_url": video_url,
        "ordem": ordem
    }
    
    aulas.append(nova_aula)
    
    if salvar_aulas(aulas):
        return nova_aula
    return None

def atualizar_aula(aula_id, titulo, resumo, video_url="", ordem=None):
    """Atualiza uma aula existente"""
    aulas = carregar_aulas()
    
    for aula in aulas:
        if aula["id"] == aula_id:
            aula["titulo"] = titulo
            aula["resumo"] = resumo
            aula["video_url"] = video_url
            if ordem is not None:
                aula["ordem"] = ordem
            return salvar_aulas(aulas)
    
    return False

def excluir_aula(aula_id):
    """Exclui uma aula"""
    aulas = carregar_aulas()
    aulas = [a for a in aulas if a["id"] != aula_id]
    return salvar_aulas(aulas)

def listar_aulas_modulo(modulo_id):
    """Lista aulas de um módulo"""
    aulas = carregar_aulas()
    return [a for a in aulas if a["modulo_id"] == modulo_id]

def obter_aula(aula_id):
    """Obtém uma aula específica"""
    aulas = carregar_aulas()
    return next((a for a in aulas if a["id"] == aula_id), None)
