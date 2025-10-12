import customtkinter as ctk
from ..components.list_section import criar_secao_lista
from ..components.cadastro_dialog import criar_janela_cadastro
from controller import cadastrar_professor, listar_professores

def create_professor_tab(tab):
    # Seção de Lista
    colunas_prof = ('id', 'nome', 'sobrenome', 'email')
    larguras_prof = (50, 150, 150, 200)
    frame_lista_prof, tabela_prof = criar_secao_lista(tab, "Lista de Professores", 
                                                     colunas_prof, larguras_prof)
    
    def atualizar_lista_prof():
        response = listar_professores()
        if response["status"] == "ok":
            tabela_prof.clear()
            for prof in response["data"]:
                tabela_prof.insert('', 'end', values=(
                    prof['id'],
                    prof['nome'],
                    prof['sobrenome'],
                    prof['email']
                ))

    def abrir_cadastro_prof():
        campos_prof = [
            {'name': 'nome', 'placeholder': 'Nome'},
            {'name': 'sobrenome', 'placeholder': 'Sobrenome'},
            {'name': 'email', 'placeholder': 'E-mail'},
            {'name': 'senha', 'placeholder': 'Senha', 'password': True},
            {'name': 'confirme_senha', 'placeholder': 'Confirme Senha', 'password': True}
        ]
        
        def cadastrar_prof_handler(**kwargs):
            response = cadastrar_professor(**kwargs)
            if response["status"] == "ok":
                atualizar_lista_prof()
            return response
        
        criar_janela_cadastro(tab, "Cadastrar Professor", 
                            cadastrar_prof_handler, campos_prof)
    
    # Botões de ação
    frame_botoes = ctk.CTkFrame(frame_lista_prof)
    frame_botoes.pack(fill="x", padx=5, pady=5)
    
    ctk.CTkButton(frame_botoes, text="Atualizar Lista", 
                 command=atualizar_lista_prof).pack(side="left", padx=5)
    ctk.CTkButton(frame_botoes, text="Novo Professor", 
                 command=abrir_cadastro_prof).pack(side="left", padx=5)

    # Carregar lista inicial
    atualizar_lista_prof()

    return frame_lista_prof