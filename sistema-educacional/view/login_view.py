import tkinter as tk
from controller.login_controller import tentar_login

def criar_tela_login(root, callback_sucesso):
    tk.Label(root, text="Usuário:").grid(row=0, column=0)
    entry_user = tk.Entry(root)
    entry_user.grid(row=0, column=1)

    tk.Label(root, text="Senha:").grid(row=1, column=0)
    entry_pass = tk.Entry(root, show="*")
    entry_pass.grid(row=1, column=1)

    label_result = tk.Label(root, text="")
    label_result.grid(row=3, column=0, columnspan=2)

    def acao_login():
        username = entry_user.get()
        password = entry_pass.get()

        resposta = tentar_login(username, password)

        if resposta["status"] == "ok":
            callback_sucesso(username)
        else:
            label_result.config(text=resposta["message"])

    btn_login = tk.Button(root, text="Login", command=acao_login)
    btn_login.grid(row=2, column=0, columnspan=2)
