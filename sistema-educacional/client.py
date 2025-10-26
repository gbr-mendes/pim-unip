import customtkinter as ctk
from view.login_view import criar_tela_login
from session import set_usuario, get_usuario, limpar_usuario

root = None

def on_login_sucesso(usuario):
    # Salva globalmente
    set_usuario(usuario)

    limpar_tela()

    role = usuario["role"]
    label = ctk.CTkLabel(
        root,
        text=f"Bem-vindo, {usuario['username']}! 👋",
        font=ctk.CTkFont(size=18, weight="bold")
    )
    label.pack(pady=30)

    # Redireciona para dashboard de acordo com role
    if role == "professor":
        mostrar_dashboard_professor()
    elif role == "aluno":
        mostrar_dashboard_aluno()
    elif role == "admin":
        mostrar_dashboard_admin()
    else:
        mostrar_dashboard_padrao()

    btn_logout = ctk.CTkButton(
        root,
        text="Sair",
        width=120,
        height=35,
        command=logout
    )
    btn_logout.pack(pady=10)

def mostrar_login():
    limpar_tela()
    criar_tela_login(root, on_login_sucesso)

def mostrar_dashboard_professor():
    from view.professor.dashboard import criar_dashboard_professor
    criar_dashboard_professor(root)

def mostrar_dashboard_aluno():
    label = ctk.CTkLabel(root, text="Dashboard do Aluno", font=ctk.CTkFont(size=16))
    label.pack(pady=20)

def mostrar_dashboard_admin():
    from view.admin import criar_dashboard_admin
    criar_dashboard_admin(root)

def mostrar_dashboard_padrao():
    label = ctk.CTkLabel(root, text="Role inexistente", font=ctk.CTkFont(size=16))
    label.pack(pady=20)

def logout():
    limpar_usuario()
    mostrar_login()

def limpar_tela():
    for widget in root.winfo_children():
        widget.destroy()

def main():
    global root

    # Configuração visual global
    ctk.set_appearance_mode("dark")          # "light" ou "dark"
    ctk.set_default_color_theme("dark-blue") # "blue", "green", "dark-blue"

    root = ctk.CTk()
    root.title("Sistema Educacional - Cliente")
    # root.geometry("700x500")
    # full size screen
    # root.state('zoomed')
    # root.minsize(600, 400)
    largura = root.winfo_screenwidth()
    altura = root.winfo_screenheight()
    x = (root.winfo_screenwidth() // 2) - (largura // 2)
    y = (root.winfo_screenheight() // 2) - (altura // 2)

    # define tamanho + posição
    root.geometry(f"{largura}x{altura}+{x}+{y}")
    root.configure(fg_color=("#1c1c1c", "#1c1c1c"))  # fundo escuro uniforme

    mostrar_login()
    root.mainloop()

if __name__ == "__main__":
    main()
