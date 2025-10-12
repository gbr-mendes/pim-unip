import customtkinter as ctk
from ..components.list_section import criar_secao_lista
from ..components.cadastro_dialog import criar_janela_cadastro
from controller import (
    cadastrar_disciplina,
    listar_disciplinas,
    listar_professores,
    listar_cursos,
    atribuir_professor_disciplina,
    associar_disciplina_curso
)

def create_discipline_tab(tab):
    # Seção de Lista
    colunas_disciplinas = ('id', 'nome')
    larguras_disciplinas = (50, 400)
    frame_lista_disciplinas, tabela_disciplinas = criar_secao_lista(tab, 
                                                                   "Lista de Disciplinas", 
                                                                   colunas_disciplinas, 
                                                                   larguras_disciplinas)
    
    def atualizar_lista_disciplinas():
        response = listar_disciplinas()
        if response["status"] == "ok":
            tabela_disciplinas.clear()
            for disciplina in response["data"]:
                tabela_disciplinas.insert('', 'end', values=(
                    disciplina['id'],
                    disciplina['nome']
                ))

    def abrir_cadastro_disciplina():
        # Obter lista de professores e cursos
        response_profs = listar_professores()
        professores = response_profs["data"] if response_profs["status"] == "ok" else []
        
        response_cursos = listar_cursos()
        cursos = response_cursos["data"] if response_cursos["status"] == "ok" else []
        
        campos_disciplina = [
            {'name': 'nome', 'placeholder': 'Nome da Disciplina'},
            {'name': 'professor_id', 'type': 'select', 'label': 'Selecione o Professor:', 'options': professores},
            {'name': 'curso_id', 'type': 'select', 'label': 'Selecione o Curso:', 'options': cursos}
        ]
        
        def cadastrar_disciplina_handler(**kwargs):
            professor_id = kwargs.pop('professor_id', None)
            curso_id = kwargs.pop('curso_id', None)
            response = cadastrar_disciplina(kwargs['nome'])
            
            if response["status"] == "ok":
                disciplina_id = response["data"]["id"]
                # Associar professor e curso à disciplina
                if professor_id:
                    atribuir_professor_disciplina(professor_id, disciplina_id)
                if curso_id:
                    associar_disciplina_curso(disciplina_id, curso_id)
                atualizar_lista_disciplinas()
            return response
        
        criar_janela_cadastro(tab, "Cadastrar Disciplina", 
                            cadastrar_disciplina_handler, campos_disciplina)
    
    # Botões de ação
    frame_botoes = ctk.CTkFrame(frame_lista_disciplinas)
    frame_botoes.pack(fill="x", padx=5, pady=5)
    
    ctk.CTkButton(frame_botoes, text="Atualizar Lista", 
                 command=atualizar_lista_disciplinas).pack(side="left", padx=5)
    ctk.CTkButton(frame_botoes, text="Nova Disciplina", 
                 command=abrir_cadastro_disciplina).pack(side="left", padx=5)

    # Carregar lista inicial
    atualizar_lista_disciplinas()

    return frame_lista_disciplinas