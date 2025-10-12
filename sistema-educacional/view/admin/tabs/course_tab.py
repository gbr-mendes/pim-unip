import customtkinter as ctk
from ..components.list_section import criar_secao_lista
from ..components.cadastro_dialog import criar_janela_cadastro
from controller import cadastrar_curso, listar_cursos

def create_course_tab(tab):
    # Seção de Lista
    colunas_cursos = ('id', 'nome')
    larguras_cursos = (50, 400)
    frame_lista_cursos, tabela_cursos = criar_secao_lista(tab, "Lista de Cursos", 
                                                         colunas_cursos, larguras_cursos)
    
    def atualizar_lista_cursos():
        response = listar_cursos()
        if response["status"] == "ok":
            tabela_cursos.clear()
            for curso in response["data"]:
                tabela_cursos.insert('', 'end', values=(
                    curso['id'],
                    curso['nome']
                ))

    def abrir_cadastro_curso():
        campos_curso = [
            {'name': 'nome', 'placeholder': 'Nome do Curso'}
        ]
        
        def cadastrar_curso_handler(**kwargs):
            response = cadastrar_curso(kwargs['nome'])
            if response["status"] == "ok":
                atualizar_lista_cursos()
            return response
        
        criar_janela_cadastro(tab, "Cadastrar Curso", 
                            cadastrar_curso_handler, campos_curso)
    
    # Botões de ação
    frame_botoes = ctk.CTkFrame(frame_lista_cursos)
    frame_botoes.pack(fill="x", padx=5, pady=5)
    
    ctk.CTkButton(frame_botoes, text="Atualizar Lista", 
                 command=atualizar_lista_cursos).pack(side="left", padx=5)
    ctk.CTkButton(frame_botoes, text="Novo Curso", 
                 command=abrir_cadastro_curso).pack(side="left", padx=5)

    # Carregar lista inicial
    atualizar_lista_cursos()

    return frame_lista_cursos