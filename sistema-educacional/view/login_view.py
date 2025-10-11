import customtkinter as ctk
import threading
from controller.login_controller import tentar_login


def criar_tela_login(root, on_login_sucesso):
    # Remove widgets anteriores
    for widget in root.winfo_children():
        widget.destroy()

    # Container principal (centralizado e responsivo)
    container = ctk.CTkFrame(root, corner_radius=15)
    container.grid(row=0, column=0, sticky="nsew", padx=60, pady=60)

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    container.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
    container.grid_columnconfigure((0, 1), weight=1)

    titulo = ctk.CTkLabel(
        container,
        text="Bem-vindo 👋",
        font=ctk.CTkFont(size=22, weight="bold")
    )
    titulo.grid(row=0, column=0, columnspan=2, pady=(20, 30))

    label_usuario = ctk.CTkLabel(container, text="Usuário:")
    label_usuario.grid(row=1, column=0, sticky="e", padx=(20, 10))
    entry_usuario = ctk.CTkEntry(container, placeholder_text="Digite seu usuário")
    entry_usuario.grid(row=1, column=1, sticky="w", padx=(10, 20))

    label_senha = ctk.CTkLabel(container, text="Senha:")
    label_senha.grid(row=2, column=0, sticky="e", padx=(20, 10))
    entry_senha = ctk.CTkEntry(container, placeholder_text="Digite sua senha", show="*")
    entry_senha.grid(row=2, column=1, sticky="w", padx=(10, 20))

    erro = ctk.CTkLabel(container, text="", font=ctk.CTkFont(size=12))
    erro.grid(row=3, column=0, columnspan=2, pady=(10, 0))

    spinner = ctk.CTkProgressBar(container, mode="indeterminate")
    spinner.grid(row=4, column=0, columnspan=2, pady=(10, 0))
    spinner.grid_remove()  # escondido no início

    btn_entrar = ctk.CTkButton(container, text="Entrar", width=120, height=35)
    btn_entrar.grid(row=5, column=0, columnspan=2, pady=(20, 40))

    def mostrar_spinner():
        spinner.grid()
        spinner.start()  # inicia a animação
        erro.configure(text="")
        btn_entrar.configure(state="disabled", text="Entrando...")

    def esconder_spinner():
        spinner.stop()  # para a animação
        spinner.grid_remove()
        btn_entrar.configure(state="normal", text="Entrar")

    def realizar_login():
        usuario = entry_usuario.get().strip()
        senha = entry_senha.get().strip()

        if not usuario or not senha:
            erro.configure(text="Preencha todos os campos", text_color="red")
            return

        mostrar_spinner()

        def tarefa_login():
            try:
                resposta = tentar_login(usuario, senha)
            except Exception as e:
                resposta = {"status": "error", "message": str(e)}

            root.after(0, lambda: tratar_resposta(resposta))

        threading.Thread(target=tarefa_login, daemon=True).start()

    def tratar_resposta(resposta):
        esconder_spinner()

        status = resposta.get("status")
        msg = resposta.get("message", "")

        if status == "ok":
            on_login_sucesso(entry_usuario.get())
        elif status == "error":
            erro.configure(text=msg or "Falha de autenticação", text_color="red")
        else:
            erro.configure(text="Resposta inesperada do servidor", text_color="red")

    btn_entrar.configure(command=realizar_login)
