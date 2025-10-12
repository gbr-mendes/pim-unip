# Admin Controller
from .admin_controller import (
    listar_admins,
    cadastrar_admin
)

# Student Controller
from .student_controller import (
    listar_alunos,
    cadastrar_aluno
)

# Professor Controller
from .professor_controller import (
    listar_professores,
    cadastrar_professor,
    atribuir_professor_disciplina
)

# Course Controller
from .course_controller import (
    listar_cursos,
    cadastrar_curso
)

# Discipline Controller
from .discipline_controller import (
    listar_disciplinas,
    cadastrar_disciplina,
    associar_disciplina_curso
)

# Class Controller
from .class_controller import (
    listar_turmas,
    criar_turma,
    associar_turma_curso,
    atribuir_aluno_turma,
    associar_disciplina_turma
)

# Export all functions
__all__ = [
    # Admin functions
    'listar_admins',
    'cadastrar_admin',
    
    # Student functions
    'listar_alunos',
    'cadastrar_aluno',
    
    # Professor functions
    'listar_professores',
    'cadastrar_professor',
    'atribuir_professor_disciplina',
    
    # Course functions
    'listar_cursos',
    'cadastrar_curso',
    
    # Discipline functions
    'listar_disciplinas',
    'cadastrar_disciplina',
    'associar_disciplina_curso',
    
    # Class functions
    'listar_turmas',
    'criar_turma',
    'associar_turma_curso',
    'atribuir_aluno_turma',
    'associar_disciplina_turma'
]
