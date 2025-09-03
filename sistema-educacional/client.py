import tkinter as tk
from view.login_view import criar_tela_login

root = None

def mostrar_login():
    limpar_tela()
    criar_tela_login(root, on_login_sucesso)

def on_login_sucesso(usuario):
    limpar_tela()

    label = tk.Label(root, text=f"Bem-vindo, {usuario}!", font=("Arial", 14))
    label.pack(pady=20)

    btn_logout = tk.Button(root, text="Sair", command=mostrar_login)
    btn_logout.pack(pady=10)

def limpar_tela():
    for widget in root.winfo_children():
        widget.destroy()

def main():
    global root
    root = tk.Tk()
    root.title("Sistema Educacional - Cliente")
    mostrar_login()
    root.mainloop()

if __name__ == "__main__":
    main()
