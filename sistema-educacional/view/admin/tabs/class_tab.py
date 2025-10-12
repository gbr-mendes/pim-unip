import customtkinter as ctk
from ..components.list_section import criar_secao_lista
from ..components.multi_select import MultiSelectComboBox
from controller import criar_turma, listar_turmas, listar_cursos, listar_disciplinas

def create_class_tab(tab):
    # Seção de Lista
    colunas_turmas = ('id', 'nome')
    larguras_turmas = (50, 400)
    frame_lista_turmas, tabela_turmas = criar_secao_lista(tab, "Lista de Turmas", 
                                                         colunas_turmas, larguras_turmas)
    
    def atualizar_lista_turmas():
        response = listar_turmas()
        if response["status"] == "ok":
            tabela_turmas.clear()
            for turma in response["data"]:
                tabela_turmas.insert('', 'end', values=(
                    turma['id'],
                    turma['nome']
                ))

    def abrir_cadastro_turma():
        # Obter lista de cursos
        response_cursos = listar_cursos()
        cursos = response_cursos["data"] if response_cursos["status"] == "ok" else []
        
        def get_disciplinas(curso_id):
            response_disciplinas = listar_disciplinas()
            return response_disciplinas["data"] if response_disciplinas["status"] == "ok" else []
        
        # Definir os campos do formulário
        campos = [
            {
                'name': 'nome_turma',
                'type': 'text',
                'label': 'Nome da Turma',
                'placeholder': 'Digite o nome da turma'
            },
            {
                'name': 'curso_id',
                'type': 'select',
                'label': 'Selecione o Curso',
                'options': cursos,
                'dependents': [
                    {
                        'name': 'disciplinas_ids',
                        'update_options': get_disciplinas
                    }
                ]
            },
            {
                'name': 'disciplinas_ids',
                'type': 'select',
                'label': 'Selecione as Disciplinas',
                'options': [],
                'multi_select': True
            }
        ]
        
        def callback_cadastro(nome_turma, curso_id, disciplinas_ids):
            response = criar_turma(
                nome_turma=nome_turma,
                curso_id=curso_id,
                disciplinas_ids=disciplinas_ids
            )
            
            if response["status"] == "ok":
                atualizar_lista_turmas()
            return response
        
        from ..components.cadastro_dialog import criar_janela_cadastro
        criar_janela_cadastro(
            frame_lista_turmas,
            "Criar Nova Turma",
            callback_cadastro,
            campos
        )
    
    # Botões de ação
    frame_botoes = ctk.CTkFrame(frame_lista_turmas)
    frame_botoes.pack(fill="x", padx=5, pady=5)
    
    ctk.CTkButton(frame_botoes, text="Atualizar Lista", 
                 command=atualizar_lista_turmas).pack(side="left", padx=5)
    ctk.CTkButton(frame_botoes, text="Nova Turma", 
                 command=abrir_cadastro_turma).pack(side="left", padx=5)

    # Carregar lista inicial
    atualizar_lista_turmas()

    return frame_lista_turmas