import customtkinter as ctk
from ..components.list_section import criar_secao_lista
from ..components.cadastro_dialog import criar_janela_cadastro
from controller import cadastrar_aluno, listar_alunos, listar_cursos, listar_turmas, atribuir_aluno_turma

def create_student_tab(tab):
    # Seção de Lista
    colunas_alunos = ('id', 'nome', 'sobrenome', 'email')
    larguras_alunos = (50, 150, 150, 200)
    frame_lista_alunos, tabela_alunos = criar_secao_lista(tab, "Lista de Alunos", 
                                                         colunas_alunos, larguras_alunos)
    
    def atualizar_lista_alunos():
        response = listar_alunos()
        if response["status"] == "ok":
            tabela_alunos.clear()
            for aluno in response["data"]:
                tabela_alunos.insert('', 'end', values=(
                    aluno['id'],
                    aluno['nome'],
                    aluno['sobrenome'],
                    aluno['email']
                ))

    def abrir_cadastro_aluno():
        # Obter lista de cursos
        response_cursos = listar_cursos()
        cursos = response_cursos["data"] if response_cursos["status"] == "ok" else []
        
        # Função para atualizar turmas baseado no curso selecionado
        def get_turmas_by_curso(curso_id):
            response_turmas = listar_turmas()
            if response_turmas["status"] == "ok":
                # Filtrar turmas pelo curso selecionado
                turmas_do_curso = [
                    turma for turma in response_turmas["data"] 
                    if turma.get('curso_id') == curso_id
                ]
                return turmas_do_curso
            return []
        
        campos_aluno = [
            {'name': 'nome', 'placeholder': 'Nome'},
            {'name': 'sobrenome', 'placeholder': 'Sobrenome'},
            {'name': 'email', 'placeholder': 'E-mail'},
            {'name': 'senha', 'placeholder': 'Senha', 'password': True},
            {'name': 'confirme_senha', 'placeholder': 'Confirme Senha', 'password': True},
            {
                'name': 'curso_id',
                'type': 'select',
                'label': 'Selecione o Curso:',
                'options': cursos,
                'dependents': [{
                    'name': 'turma_id',
                    'update_options': get_turmas_by_curso
                }]
            },
            {
                'name': 'turma_id',
                'type': 'select',
                'label': 'Selecione a Turma:',
                'options': []  # Será preenchido após selecionar o curso
            }
        ]
        
        def cadastrar_aluno_handler(**kwargs):
            turma_id = kwargs.pop('turma_id', None)
            curso_id = kwargs.pop('curso_id', None)  # Remove curso_id pois não é usado no cadastro
            response = cadastrar_aluno(**kwargs)
            if response["status"] == "ok" and turma_id:
                # Atribuir aluno à turma
                atribuir_aluno_turma(response["data"]["id"], turma_id)
                atualizar_lista_alunos()
            return response
        
        criar_janela_cadastro(tab, "Cadastrar Aluno", 
                            cadastrar_aluno_handler, campos_aluno)
    
    # Botões de ação
    frame_botoes = ctk.CTkFrame(frame_lista_alunos)
    frame_botoes.pack(fill="x", padx=5, pady=5)
    
    ctk.CTkButton(frame_botoes, text="Atualizar Lista", 
                 command=atualizar_lista_alunos).pack(side="left", padx=5)
    ctk.CTkButton(frame_botoes, text="Novo Aluno", 
                 command=abrir_cadastro_aluno).pack(side="left", padx=5)

    # Carregar lista inicial
    atualizar_lista_alunos()

    return frame_lista_alunos