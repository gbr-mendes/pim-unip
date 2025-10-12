import customtkinter as ctk
from ..components.list_section import criar_secao_lista
from ..components.cadastro_dialog import criar_janela_cadastro
from controller import cadastrar_admin, listar_admins

def create_admin_tab(tab):
    # Seção de Lista
    colunas_admin = ('id', 'nome', 'sobrenome', 'email')
    larguras_admin = (50, 150, 150, 200)
    frame_lista_admin, tabela_admin = criar_secao_lista(tab, "Lista de Administradores", 
                                                       colunas_admin, larguras_admin)
    
    def atualizar_lista_admin():
        response = listar_admins()
        if response["status"] == "ok":
            tabela_admin.clear()
            for admin in response["data"]:
                tabela_admin.insert('', 'end', values=(
                    admin['id'],
                    admin['nome'],
                    admin['sobrenome'],
                    admin['email']
                ))

    def abrir_cadastro_admin():
        campos_admin = [
            {'name': 'nome', 'placeholder': 'Nome'},
            {'name': 'sobrenome', 'placeholder': 'Sobrenome'},
            {'name': 'email', 'placeholder': 'E-mail'},
            {'name': 'senha', 'placeholder': 'Senha', 'password': True},
            {'name': 'confirme_senha', 'placeholder': 'Confirme Senha', 'password': True}
        ]
        
        def cadastrar_admin_handler(**kwargs):
            response = cadastrar_admin(**kwargs)
            if response["status"] == "ok":
                atualizar_lista_admin()
            return response
        
        criar_janela_cadastro(tab, "Cadastrar Administrador", 
                            cadastrar_admin_handler, campos_admin)
    
    # Botões de ação
    frame_botoes = ctk.CTkFrame(frame_lista_admin)
    frame_botoes.pack(fill="x", padx=5, pady=5)
    
    ctk.CTkButton(frame_botoes, text="Atualizar Lista", 
                 command=atualizar_lista_admin).pack(side="left", padx=5)
    ctk.CTkButton(frame_botoes, text="Novo Administrador", 
                 command=abrir_cadastro_admin).pack(side="left", padx=5)

    # Carregar lista inicial
    atualizar_lista_admin()

    return frame_lista_admin