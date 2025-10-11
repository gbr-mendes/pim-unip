import customtkinter as ctk
from controller.admin_controller import (
    cadastrar_aluno,
    cadastrar_professor,
    cadastrar_admin,
    criar_turma,
    atribuir_aluno_turma,
    cadastrar_curso,
    cadastrar_disciplina,
    associar_disciplina_curso,
    atribuir_professor_disciplina,
    associar_turma_curso,
    associar_disciplina_turma
)

def mostrar_feedback(frame, mensagem, tipo="error", row=None):
    """Mostra feedback ao usuário com cor apropriada"""
    # Remove feedback anterior se existir
    for widget in frame.winfo_children():
        if isinstance(widget, ctk.CTkLabel) and hasattr(widget, 'feedback_label'):
            widget.destroy()
    
    # Configura cor baseada no tipo
    cor = "#FF4444" if tipo == "error" else "#4CAF50"
    
    # Cria label de feedback
    feedback = ctk.CTkLabel(frame, text=mensagem, text_color=cor)
    feedback.feedback_label = True  # marca como label de feedback
    
    if row is not None:
        feedback.grid(row=row, column=0, columnspan=2, pady=(5, 10))
    else:
        feedback.pack(pady=(5, 10))

def limpar_campos(*entries):
    """Limpa os campos de entrada especificados"""
    for entry in entries:
        entry.delete(0, 'end')

def processar_resposta(response, frame, campos, row_feedback=None):
    """Processa a resposta do controller e atualiza a UI"""
    if response["status"] == "ok":
        mostrar_feedback(frame, response["message"], "success", row_feedback)
        if response.get("clear_form", False):
            limpar_campos(*campos)
    else:
        mostrar_feedback(frame, response["message"], "error", row_feedback)

def criar_dashboard_admin(root):
    # Limpa tela
    for widget in root.winfo_children():
        widget.destroy()

    # Container principal
    container = ctk.CTkFrame(root, corner_radius=15)
    container.pack(pady=20, padx=40, fill="both", expand=True)

    titulo = ctk.CTkLabel(container, text="Dashboard do Admin", font=ctk.CTkFont(size=22, weight="bold"))
    titulo.pack(pady=20)

    # Tabview principal
    tabview = ctk.CTkTabview(container, height=500)
    tabview.pack(pady=10, fill="both", expand=True)

    # Criar abas
    tabview.add("Administradores")
    tabview.add("Alunos")
    tabview.add("Professores")
    tabview.add("Cursos")
    tabview.add("Disciplinas")
    tabview.add("Turmas")
    tabview.add("Atribuições")

    # Função de centralização
    def centralizar(frame, widget, row, columnspan=2, pady=(5,5), max_width=400):
        if isinstance(widget, (ctk.CTkEntry, ctk.CTkButton)):
            widget.configure(width=max_width)
        widget.grid(row=row, column=0, columnspan=columnspan, pady=pady)
        frame.grid_columnconfigure(0, weight=1)
        if columnspan > 1:
            frame.grid_columnconfigure(1, weight=1)

    # ====================================================
    # --- ABA ADMINISTRADORES ---
    # ====================================================
    frame_admin = tabview.tab("Administradores")

    centralizar(frame_admin, ctk.CTkLabel(frame_admin, text="Cadastrar Administrador:"), 0, pady=(10,10))

    entry_nome_admin = ctk.CTkEntry(frame_admin, placeholder_text="Nome")
    centralizar(frame_admin, entry_nome_admin, 1)
    entry_sobrenome_admin = ctk.CTkEntry(frame_admin, placeholder_text="Sobrenome")
    centralizar(frame_admin, entry_sobrenome_admin, 2)
    entry_email_admin = ctk.CTkEntry(frame_admin, placeholder_text="E-mail")
    centralizar(frame_admin, entry_email_admin, 3)
    entry_senha_admin = ctk.CTkEntry(frame_admin, placeholder_text="Senha", show="*")
    centralizar(frame_admin, entry_senha_admin, 4)
    entry_confirme_senha_admin = ctk.CTkEntry(frame_admin, placeholder_text="Confirme Senha", show="*")
    centralizar(frame_admin, entry_confirme_senha_admin, 5)

    btn_cadastrar_admin = ctk.CTkButton(
        frame_admin,
        text="Cadastrar",
        command=lambda: processar_resposta(
            cadastrar_admin(
                entry_nome_admin.get(),
                entry_sobrenome_admin.get(),
                entry_email_admin.get(),
                entry_senha_admin.get(),
                entry_confirme_senha_admin.get()
            ),
            frame_admin,
            [entry_nome_admin, entry_sobrenome_admin, entry_email_admin, 
             entry_senha_admin, entry_confirme_senha_admin],
            7
        )
    )
    centralizar(frame_admin, btn_cadastrar_admin, 6, pady=(10,5))

    # ====================================================
    # --- ABA ALUNOS ---
    # ====================================================
    frame_alunos = tabview.tab("Alunos")

    centralizar(frame_alunos, ctk.CTkLabel(frame_alunos, text="Cadastrar Aluno:"), 0, pady=(10,10))

    entry_nome_aluno = ctk.CTkEntry(frame_alunos, placeholder_text="Nome")
    centralizar(frame_alunos, entry_nome_aluno, 1)
    entry_sobrenome_aluno = ctk.CTkEntry(frame_alunos, placeholder_text="Sobrenome")
    centralizar(frame_alunos, entry_sobrenome_aluno, 2)
    entry_email_aluno = ctk.CTkEntry(frame_alunos, placeholder_text="E-mail")
    centralizar(frame_alunos, entry_email_aluno, 3)
    entry_senha_aluno = ctk.CTkEntry(frame_alunos, placeholder_text="Senha Padrão", show="*")
    centralizar(frame_alunos, entry_senha_aluno, 4)
    entry_confirme_senha_aluno = ctk.CTkEntry(frame_alunos, placeholder_text="Confirme Senha", show="*")
    centralizar(frame_alunos, entry_confirme_senha_aluno, 5)

    btn_cadastrar_aluno = ctk.CTkButton(
        frame_alunos,
        text="Cadastrar",
        command=lambda: processar_resposta(
            cadastrar_aluno(
                entry_nome_aluno.get(),
                entry_sobrenome_aluno.get(),
                entry_email_aluno.get(),
                entry_senha_aluno.get(),
                entry_confirme_senha_aluno.get()
            ),
            frame_alunos,
            [entry_nome_aluno, entry_sobrenome_aluno, entry_email_aluno, 
             entry_senha_aluno, entry_confirme_senha_aluno],
            7
        )
    )
    centralizar(frame_alunos, btn_cadastrar_aluno, 6, pady=(10,5))

    # ====================================================
    # --- ABA PROFESSORES ---
    # ====================================================
    frame_prof = tabview.tab("Professores")

    centralizar(frame_prof, ctk.CTkLabel(frame_prof, text="Cadastrar Professor:"), 0, pady=(10,10))

    entry_nome_prof = ctk.CTkEntry(frame_prof, placeholder_text="Nome")
    centralizar(frame_prof, entry_nome_prof, 1)
    entry_sobrenome_prof = ctk.CTkEntry(frame_prof, placeholder_text="Sobrenome")
    centralizar(frame_prof, entry_sobrenome_prof, 2)
    entry_email_prof = ctk.CTkEntry(frame_prof, placeholder_text="E-mail")
    centralizar(frame_prof, entry_email_prof, 3)
    entry_senha_prof = ctk.CTkEntry(frame_prof, placeholder_text="Senha Padrão", show="*")
    centralizar(frame_prof, entry_senha_prof, 4)
    entry_confirme_senha_prof = ctk.CTkEntry(frame_prof, placeholder_text="Confirme Senha", show="*")
    centralizar(frame_prof, entry_confirme_senha_prof, 5)

    btn_cadastrar_prof = ctk.CTkButton(
        frame_prof,
        text="Cadastrar",
        command=lambda: processar_resposta(
            cadastrar_professor(
                entry_nome_prof.get(),
                entry_sobrenome_prof.get(),
                entry_email_prof.get(),
                entry_senha_prof.get(),
                entry_confirme_senha_prof.get()
            ),
            frame_prof,
            [entry_nome_prof, entry_sobrenome_prof, entry_email_prof,
             entry_senha_prof, entry_confirme_senha_prof],
            7
        )
    )
    centralizar(frame_prof, btn_cadastrar_prof, 6, pady=(10,5))

    # ====================================================
    # --- ABA CURSOS ---
    # ====================================================
    frame_cursos = tabview.tab("Cursos")
    centralizar(frame_cursos, ctk.CTkLabel(frame_cursos, text="Cadastrar Curso:"), 0, pady=(10,10))

    entry_nome_curso = ctk.CTkEntry(frame_cursos, placeholder_text="Nome do Curso")
    centralizar(frame_cursos, entry_nome_curso, 1)

    btn_cadastrar_curso = ctk.CTkButton(
        frame_cursos, text="Cadastrar",
        command=lambda: processar_resposta(
            cadastrar_curso(entry_nome_curso.get()),
            frame_cursos,
            [entry_nome_curso],
            3
        )
    )
    centralizar(frame_cursos, btn_cadastrar_curso, 2, pady=(10,5))

    # ====================================================
    # --- ABA DISCIPLINAS ---
    # ====================================================
    frame_disciplinas = tabview.tab("Disciplinas")

    centralizar(frame_disciplinas, ctk.CTkLabel(frame_disciplinas, text="Cadastrar Disciplina:"), 0, pady=(10,10))
    entry_nome_disciplina = ctk.CTkEntry(frame_disciplinas, placeholder_text="Nome da Disciplina")
    centralizar(frame_disciplinas, entry_nome_disciplina, 1)

    btn_cadastrar_disciplina = ctk.CTkButton(
        frame_disciplinas, text="Cadastrar",
        command=lambda: processar_resposta(
            cadastrar_disciplina(entry_nome_disciplina.get()),
            frame_disciplinas,
            [entry_nome_disciplina],
            3
        )
    )
    centralizar(frame_disciplinas, btn_cadastrar_disciplina, 2, pady=(10,5))

    # Associação Disciplina ↔ Curso
    centralizar(frame_disciplinas, ctk.CTkLabel(frame_disciplinas, text="Associar Disciplina ao Curso:"), 4, pady=(20,5))

    linha_disc_curso = ctk.CTkFrame(frame_disciplinas)
    linha_disc_curso.grid(row=5, column=0, columnspan=2, pady=(5,5))

    entry_id_disciplina = ctk.CTkEntry(linha_disc_curso, placeholder_text="ID da Disciplina", width=180)
    entry_id_disciplina.pack(side="left", padx=5)
    entry_id_curso = ctk.CTkEntry(linha_disc_curso, placeholder_text="ID do Curso", width=180)
    entry_id_curso.pack(side="left", padx=5)

    btn_assoc_disc_curso = ctk.CTkButton(
        linha_disc_curso,
        text="Associar",
        width=100,
        command=lambda: processar_resposta(
            associar_disciplina_curso(entry_id_disciplina.get(), entry_id_curso.get()),
            frame_disciplinas,
            [entry_id_disciplina, entry_id_curso],
            6
        )
    )
    btn_assoc_disc_curso.pack(side="left", padx=5)


    # ====================================================
    # --- ABA TURMAS ---
    # ====================================================
    frame_turmas = tabview.tab("Turmas")

    centralizar(frame_turmas, ctk.CTkLabel(frame_turmas, text="Criar Turma:"), 0, pady=(10,10))
    entry_nome_turma = ctk.CTkEntry(frame_turmas, placeholder_text="Nome da Turma")
    centralizar(frame_turmas, entry_nome_turma, 1)

    btn_criar_turma = ctk.CTkButton(
        frame_turmas, text="Criar",
        command=lambda: processar_resposta(
            criar_turma(entry_nome_turma.get()),
            frame_turmas,
            [entry_nome_turma],
            3
        )
    )
    centralizar(frame_turmas, btn_criar_turma, 2, pady=(10,5))

    # Associação Turma ↔ Curso
    centralizar(frame_turmas, ctk.CTkLabel(frame_turmas, text="Associar Turma ao Curso:"), 4, pady=(20,5))

    linha_turma_curso = ctk.CTkFrame(frame_turmas)
    linha_turma_curso.grid(row=5, column=0, columnspan=2, pady=(5,5))

    entry_id_turma = ctk.CTkEntry(linha_turma_curso, placeholder_text="ID da Turma", width=180)
    entry_id_turma.pack(side="left", padx=5)
    entry_id_curso_turma = ctk.CTkEntry(linha_turma_curso, placeholder_text="ID do Curso", width=180)
    entry_id_curso_turma.pack(side="left", padx=5)

    btn_assoc_turma_curso = ctk.CTkButton(
        linha_turma_curso,
        text="Associar",
        width=100,
        command=lambda: processar_resposta(
            associar_turma_curso(entry_id_turma.get(), entry_id_curso_turma.get()),
            frame_turmas,
            [entry_id_turma, entry_id_curso_turma],
            6
        )
    )
    btn_assoc_turma_curso.pack(side="left", padx=5)

    # ====================================================
    # --- ABA ATRIBUIÇÕES ---
    # ====================================================
    frame_atribuicoes = tabview.tab("Atribuições")

    # Função auxiliar para criar linha compacta de atribuição
    def linha_atribuicao(frame, texto, placeholders, comando, botao_texto="Atribuir"):
        container = ctk.CTkFrame(frame)
        container.pack(pady=5, fill="x")
        
        label = ctk.CTkLabel(container, text=texto, font=ctk.CTkFont(size=14, weight="bold"))
        label.pack(pady=(10, 5))

        linha = ctk.CTkFrame(container)
        linha.pack(pady=5)

        entries = []
        for placeholder in placeholders:
            entry = ctk.CTkEntry(linha, placeholder_text=placeholder, width=180)
            entry.pack(side="left", padx=5)
            entries.append(entry)

        btn = ctk.CTkButton(
            linha, 
            text=botao_texto, 
            width=100, 
            command=lambda: processar_resposta(
                comando(*[e.get() for e in entries]),
                container,
                entries
            )
        )
        btn.pack(side="left", padx=5)

        return entries, container

    # Atribuir aluno à turma
    linha_atribuicao(
        frame_atribuicoes,
        "Atribuir Aluno à Turma:",
        ["ID do Aluno", "ID da Turma"],
        atribuir_aluno_turma
    )

    # Atribuir professor à disciplina
    linha_atribuicao(
        frame_atribuicoes,
        "Atribuir Professor à Disciplina:",
        ["ID do Professor", "ID da Disciplina"],
        atribuir_professor_disciplina
    )

    # Associar disciplina à turma
    linha_atribuicao(
        frame_atribuicoes,
        "Associar Disciplina à Turma:",
        ["ID da Disciplina", "ID da Turma"],
        associar_disciplina_turma,
        botao_texto="Associar"
    )

