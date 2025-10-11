import time
import random

# =====================================================
# === ALUNOS ==========================================
# =====================================================

def cadastrar_aluno(nome: str, sobrenome: str, email: str, senha: str, confirme_senha: str):
    """Mock de cadastro de aluno"""
    if not nome.strip() or not sobrenome.strip() or not email.strip():
        print("Erro: Campos obrigatórios não preenchidos")
        return {"status": "error", "message": "Nome, sobrenome e email são obrigatórios"}

    if senha != confirme_senha:
        print("Erro: Senhas não conferem")
        return {"status": "error", "message": "Senhas não conferem"}

    time.sleep(0.5)
    id_aluno = random.randint(1000, 9999)
    print(f"Aluno '{nome} {sobrenome}' cadastrado com sucesso! (ID: {id_aluno})")
    return {"status": "ok", "message": f"Aluno '{nome} {sobrenome}' cadastrado", "id": id_aluno}


# =====================================================
# === PROFESSORES =====================================
# =====================================================

def cadastrar_professor(nome: str, sobrenome: str, email: str, senha: str, confirme_senha: str):
    """Mock de cadastro de professor"""
    if not nome.strip() or not sobrenome.strip() or not email.strip():
        print("Erro: Campos obrigatórios não preenchidos")
        return {"status": "error", "message": "Nome, sobrenome e email são obrigatórios"}

    if senha != confirme_senha:
        print("Erro: Senhas não conferem")
        return {"status": "error", "message": "Senhas não conferem"}

    time.sleep(0.5)
    id_prof = random.randint(1000, 9999)
    print(f"Professor '{nome} {sobrenome}' cadastrado com sucesso! (ID: {id_prof})")
    return {"status": "ok", "message": f"Professor '{nome} {sobrenome}' cadastrado", "id": id_prof}


# =====================================================
# === CURSOS ==========================================
# =====================================================

def cadastrar_curso(nome_curso: str):
    """Mock de cadastro de curso"""
    if not nome_curso.strip():
        print("Erro: Nome do curso não pode ser vazio")
        return {"status": "error", "message": "Nome do curso é obrigatório"}

    time.sleep(0.5)
    id_curso = random.randint(1000, 9999)
    print(f"Curso '{nome_curso}' cadastrado com sucesso! (ID: {id_curso})")
    return {"status": "ok", "message": f"Curso '{nome_curso}' cadastrado", "id": id_curso}


# =====================================================
# === DISCIPLINAS =====================================
# =====================================================

def cadastrar_disciplina(nome_disciplina: str):
    """Mock de cadastro de disciplina"""
    if not nome_disciplina.strip():
        print("Erro: Nome da disciplina não pode ser vazio")
        return {"status": "error", "message": "Nome da disciplina é obrigatório"}

    time.sleep(0.5)
    id_disc = random.randint(1000, 9999)
    print(f"Disciplina '{nome_disciplina}' cadastrada com sucesso! (ID: {id_disc})")
    return {"status": "ok", "message": f"Disciplina '{nome_disciplina}' cadastrada", "id": id_disc}


def associar_disciplina_curso(id_disciplina: str, id_curso: str):
    """Mock de associação de disciplina a curso"""
    if not id_disciplina.strip() or not id_curso.strip():
        return {"status": "error", "message": "Disciplina e Curso são obrigatórios"}

    time.sleep(0.5)
    print(f"Disciplina {id_disciplina} associada ao curso {id_curso}")
    return {"status": "ok", "message": f"Disciplina {id_disciplina} associada ao curso {id_curso}"}


# =====================================================
# === PROFESSOR ↔ DISCIPLINA ==========================
# =====================================================

def atribuir_professor_disciplina(id_professor: str, id_disciplina: str):
    """Mock de atribuição de professor a disciplina"""
    if not id_professor.strip() or not id_disciplina.strip():
        return {"status": "error", "message": "Professor e Disciplina são obrigatórios"}

    time.sleep(0.5)
    print(f"Professor {id_professor} atribuído à disciplina {id_disciplina}")
    return {"status": "ok", "message": f"Professor {id_professor} atribuído à disciplina {id_disciplina}"}


# =====================================================
# === TURMAS ==========================================
# =====================================================

def criar_turma(nome_turma: str):
    """Mock de criação de turma"""
    if not nome_turma.strip():
        print("Erro: Nome da turma não pode ser vazio")
        return {"status": "error", "message": "Nome da turma é obrigatório"}

    time.sleep(0.5)
    id_turma = random.randint(1000, 9999)
    print(f"Turma '{nome_turma}' criada com sucesso! (ID: {id_turma})")
    return {"status": "ok", "message": f"Turma '{nome_turma}' criada", "id": id_turma}


def associar_turma_curso(id_turma: str, id_curso: str):
    """Mock de associação de turma a curso"""
    if not id_turma.strip() or not id_curso.strip():
        return {"status": "error", "message": "Turma e Curso são obrigatórios"}

    time.sleep(0.5)
    print(f"Turma {id_turma} associada ao curso {id_curso}")
    return {"status": "ok", "message": f"Turma {id_turma} associada ao curso {id_curso}"}


# =====================================================
# === ATRIBUIÇÕES / RELAÇÕES ==========================
# =====================================================

def atribuir_aluno_turma(id_aluno: str, id_turma: str):
    """Mock de atribuição de aluno a turma"""
    if not id_aluno.strip() or not id_turma.strip():
        return {"status": "error", "message": "Aluno e Turma são obrigatórios"}

    time.sleep(0.5)
    print(f"Aluno {id_aluno} atribuído à turma {id_turma}")
    return {"status": "ok", "message": f"Aluno {id_aluno} atribuído à turma {id_turma}"}


def atribuir_materia_professor(id_materia: str, id_professor: str):
    """Mock antigo (mantido para compatibilidade)"""
    if not id_materia.strip() or not id_professor.strip():
        return {"status": "error", "message": "Matéria e Professor são obrigatórios"}

    time.sleep(0.5)
    print(f"Matéria {id_materia} atribuída ao professor {id_professor}")
    return {"status": "ok", "message": f"Matéria {id_materia} atribuída ao professor {id_professor}"}


def associar_disciplina_turma(id_disciplina: str, id_turma: str):
    """Mock de associação de disciplina à turma"""
    if not id_disciplina.strip() or not id_turma.strip():
        return {"status": "error", "message": "Disciplina e Turma são obrigatórias"}

    time.sleep(0.5)
    print(f"Disciplina {id_disciplina} associada à turma {id_turma}")
    return {"status": "ok", "message": f"Disciplina {id_disciplina} associada à turma {id_turma}"}
