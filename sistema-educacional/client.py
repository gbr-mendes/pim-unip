import customtkinter as ctk
from view.login_view import criar_tela_login

root = None

def mostrar_login():
    limpar_tela()
    criar_tela_login(root, on_login_sucesso)

def on_login_sucesso(usuario):
    limpar_tela()

    label = ctk.CTkLabel(
        root,
        text=f"Bem-vindo, {usuario}! 👋",
        font=ctk.CTkFont(size=18, weight="bold")
    )
    label.pack(pady=30)

    btn_logout = ctk.CTkButton(
        root,
        text="Sair",
        width=120,
        height=35,
        command=mostrar_login
    )
    btn_logout.pack(pady=10)

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
    root.geometry("700x500")
    root.minsize(600, 400)
    root.configure(fg_color=("#1c1c1c", "#1c1c1c"))  # fundo escuro uniforme

    mostrar_login()
    root.mainloop()

if __name__ == "__main__":
    main()
