import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
from controller import (
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
    listar_admins,
    listar_alunos,
    listar_professores,
    listar_cursos,
    listar_disciplinas,
    listar_turmas
)


class CustomTable(ttk.Treeview):
    def __init__(self, parent, columns, column_widths=None):
        super().__init__(parent, columns=columns, show='headings', selectmode='browse')

        mode = ctk.get_appearance_mode()
        theme = ctk.ThemeManager.theme

        # Cores adaptadas ao tema escuro
        base_bg = theme["CTkFrame"]["fg_color"][1 if mode == "Dark" else 0]
        entry_bg = theme["CTkEntry"]["fg_color"][1 if mode == "Dark" else 0]
        button_fg = theme["CTkButton"]["fg_color"][1 if mode == "Dark" else 0]
        text_color = theme["CTkLabel"]["text_color"][1 if mode == "Dark" else 0]
        hover_color = theme["CTkButton"]["hover_color"][1 if mode == "Dark" else 0]

        # Tons intermediários para zebra
        zebra_1 = entry_bg
        zebra_2 = self._mix_colors(entry_bg, "#202020", 0.15)

        # Estilo base
        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Custom.Treeview",
            background=entry_bg,
            fieldbackground=entry_bg,
            foreground=text_color,
            rowheight=30,
            borderwidth=0,
            relief="flat",
            font=('Segoe UI', 11)
        )

        # Mapeia seleção
        style.map(
            "Custom.Treeview",
            background=[("selected", button_fg)],
            foreground=[("selected", "white")]
        )

        # Cabeçalhos com cor próxima das abas
        style.configure(
            "Custom.Treeview.Heading",
            background=hover_color,
            foreground="white",
            font=('Segoe UI', 10, 'bold'),
            borderwidth=0,
            relief="flat"
        )

        style.map("Custom.Treeview.Heading",
                  background=[("active", button_fg)],
                  foreground=[("active", "white")])

        # Configura colunas
        for idx, col in enumerate(columns):
            width = column_widths[idx] if column_widths else 150
            self.heading(col, text=col.title())
            self.column(col, width=width, anchor="center")

        self.configure(style="Custom.Treeview")

        # Aplica zebra (linhas alternadas)
        self.tag_configure("oddrow", background=zebra_1)
        self.tag_configure("evenrow", background=zebra_2)

    def insert(self, parent, index, iid=None, **kw):
        """Insere linha com zebra automática"""
        children = self.get_children()
        row_tag = "evenrow" if len(children) % 2 == 0 else "oddrow"
        if "tags" in kw:
            kw["tags"].append(row_tag)
        else:
            kw["tags"] = (row_tag,)
        return super().insert(parent, index, iid=iid, **kw)

    def clear(self):
        for item in self.get_children():
            self.delete(item)

    def _mix_colors(self, c1, c2, ratio=0.5):
        """Mistura duas cores hex (ex: '#202020', '#404040')"""
        c1, c2 = c1.lstrip("#"), c2.lstrip("#")
        rgb1 = tuple(int(c1[i:i+2], 16) for i in (0, 2, 4))
        rgb2 = tuple(int(c2[i:i+2], 16) for i in (0, 2, 4))
        mixed = tuple(int(rgb1[i]*(1-ratio) + rgb2[i]*ratio) for i in range(3))
        return f"#{mixed[0]:02x}{mixed[1]:02x}{mixed[2]:02x}"

def criar_janela_cadastro(parent, titulo, callback_cadastro, campos):
    """Cria uma janela de cadastro sobreposta"""
    window = ctk.CTkToplevel(parent)
    window.title(titulo)
    window.geometry("400x600")
    window.transient(parent)
    window.grab_set()
    
    frame = ctk.CTkFrame(window)
    frame.pack(padx=20, pady=20, fill="both", expand=True)
    
    ctk.CTkLabel(frame, text=titulo, font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
    
    entries = {}
    dependent_fields = {}
    
    for campo in campos:
        if campo.get('type') == 'select':
            # Criar label para o select
            ctk.CTkLabel(frame, text=campo['label']).pack(fill="x", padx=20, pady=(10,0))
            # Criar combobox
            combobox = ctk.CTkComboBox(frame, values=[f"{item['id']} - {item['nome']}" for item in campo['options']])
            combobox.pack(fill="x", padx=20, pady=(0,10))
            
            if campo.get('default'):
                combobox.set(campo['default'])
                
            entries[campo['name']] = combobox
            
            # Se este campo tem dependentes, configurar o callback
            if campo.get('dependents'):
                dependent_fields[campo['name']] = campo['dependents']
                
                def on_combobox_select(choice, name=campo['name']):
                    update_dependent_fields(name)
                
                combobox.configure(command=on_combobox_select)
                
        else:
            # Campo normal de texto
            entry = ctk.CTkEntry(frame, placeholder_text=campo['placeholder'])
            entry.pack(fill="x", padx=20, pady=10)
            if campo.get('password', False):
                entry.configure(show="*")
            entries[campo['name']] = entry
    
    def update_dependent_fields(field_name):
        if field_name not in dependent_fields:
            return
            
        selected = entries[field_name].get()
        if not selected:
            return
            
        selected_id = selected.split(' - ')[0]
        
        for dep_field in dependent_fields[field_name]:
            dependent_combobox = entries[dep_field['name']]
            # Atualizar opções baseado no valor selecionado
            new_options = dep_field['update_options'](selected_id)
            if new_options:
                # Criar lista de strings formatadas para as opções
                option_strings = [f"{item['id']} - {item['nome']}" for item in new_options]
                # Atualizar valores do combobox
                dependent_combobox.configure(values=option_strings)
                # Se houver opções, selecionar a primeira
                if option_strings:
                    dependent_combobox.set(option_strings[0])
                else:
                    dependent_combobox.set("")
            else:
                dependent_combobox.configure(values=[])
                dependent_combobox.set("")
    
    def submit():
        valores = {}
        for name, widget in entries.items():
            if isinstance(widget, ctk.CTkComboBox):
                # Pegar apenas o ID do item selecionado (antes do hífen)
                valor = widget.get().split(' - ')[0] if widget.get() else None
                valores[name] = valor
            else:
                valores[name] = widget.get()
        
        response = callback_cadastro(**valores)
        if response["status"] == "ok":
            window.destroy()
        else:
            mostrar_feedback(frame, response["message"], "error")
    
    ctk.CTkButton(frame, text="Cadastrar", command=submit).pack(pady=20)
    ctk.CTkButton(frame, text="Voltar", command=window.destroy).pack(pady=5)

def criar_secao_lista(parent, titulo, colunas, larguras_colunas=None):
    """Cria uma seção com título, tabela e botões"""
    frame = ctk.CTkFrame(parent)
    frame.pack(fill="both", expand=True, padx=10, pady=5)
    
    header = ctk.CTkFrame(frame)
    header.pack(fill="x", pady=5)
    
    ctk.CTkLabel(header, text=titulo, font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", padx=5)
    
    tabela = CustomTable(frame, colunas, larguras_colunas)
    tabela.pack(fill="both", expand=True, padx=5, pady=5)
    
    return frame, tabela

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

def atualizar_lista(listbox, dados):
    """Atualiza o conteúdo de um listbox com novos dados"""
    listbox.delete('1.0', 'end')
    for item in dados:
        if isinstance(item, dict):
            # Formata string baseada no tipo de item
            if "nome" in item and "sobrenome" in item:
                texto = f"{item['nome']} {item['sobrenome']} (ID: {item['id']})"
            elif "nome" in item:
                texto = f"{item['nome']} (ID: {item['id']})"
            else:
                texto = str(item)
            listbox.insert('end', texto + '\n')
        else:
            listbox.insert('end', str(item) + '\n')

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
    tabview = ctk.CTkTabview(container, height=600)  # Aumentado para acomodar as listas
    tabview.pack(pady=10, fill="both", expand=True)

    # Criar abas
    tabview.add("Administradores")
    tabview.add("Alunos")
    tabview.add("Professores")
    tabview.add("Cursos")
    tabview.add("Disciplinas")
    tabview.add("Turmas")
    tabview.add("Atribuições")

    # ====================================================
    # --- ABA ADMINISTRADORES ---
    # ====================================================
    frame_admin = tabview.tab("Administradores")
    
    # Seção de Lista
    colunas_admin = ('id', 'nome', 'sobrenome', 'email')
    larguras_admin = (50, 150, 150, 200)
    frame_lista_admin, tabela_admin = criar_secao_lista(frame_admin, "Lista de Administradores", colunas_admin, larguras_admin)
    
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
        
        criar_janela_cadastro(frame_admin, "Cadastrar Administrador", 
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

    # ====================================================
    # --- ABA ALUNOS ---
    # ====================================================
    frame_alunos = tabview.tab("Alunos")

    # Seção de Lista
    colunas_alunos = ('id', 'nome', 'sobrenome', 'email')
    larguras_alunos = (50, 150, 150, 200)
    frame_lista_alunos, tabela_alunos = criar_secao_lista(frame_alunos, "Lista de Alunos", 
                                                         colunas_alunos, larguras_alunos)
    
    def atualizar_lista_alunos():
        response = listar_alunos()
        if response["status"] == "ok":
            tabela_alunos.clear()
            for aluno in response["data"]:
                tabela_alunos.insert('', 'end', values=(
                    aluno['id'],
                    aluno['nome'],
                    aluno['sobrenome'],
                    aluno['email']
                ))

    def abrir_cadastro_aluno():
        # Obter lista de cursos
        response_cursos = listar_cursos()
        cursos = response_cursos["data"] if response_cursos["status"] == "ok" else []
        
        # Função para atualizar turmas baseado no curso selecionado
        def get_turmas_by_curso(curso_id):
            response_turmas = listar_turmas()
            if response_turmas["status"] == "ok":
                # Filtrar turmas pelo curso selecionado
                turmas_do_curso = [
                    turma for turma in response_turmas["data"] 
                    if turma.get('curso_id') == curso_id
                ]
                return turmas_do_curso
            return []
        
        campos_aluno = [
            {'name': 'nome', 'placeholder': 'Nome'},
            {'name': 'sobrenome', 'placeholder': 'Sobrenome'},
            {'name': 'email', 'placeholder': 'E-mail'},
            {'name': 'senha', 'placeholder': 'Senha', 'password': True},
            {'name': 'confirme_senha', 'placeholder': 'Confirme Senha', 'password': True},
            {
                'name': 'curso_id',
                'type': 'select',
                'label': 'Selecione o Curso:',
                'options': cursos,
                'dependents': [{
                    'name': 'turma_id',
                    'update_options': get_turmas_by_curso
                }]
            },
            {
                'name': 'turma_id',
                'type': 'select',
                'label': 'Selecione a Turma:',
                'options': []  # Será preenchido após selecionar o curso
            }
        ]
        
        def cadastrar_aluno_handler(**kwargs):
            turma_id = kwargs.pop('turma_id', None)
            curso_id = kwargs.pop('curso_id', None)  # Remove curso_id pois não é usado no cadastro
            response = cadastrar_aluno(**kwargs)
            if response["status"] == "ok" and turma_id:
                # Atribuir aluno à turma
                atribuir_aluno_turma(response["data"]["id"], turma_id)
                atualizar_lista_alunos()
            return response
        
        criar_janela_cadastro(frame_alunos, "Cadastrar Aluno", 
                            cadastrar_aluno_handler, campos_aluno)
    
    # Botões de ação
    frame_botoes = ctk.CTkFrame(frame_lista_alunos)
    frame_botoes.pack(fill="x", padx=5, pady=5)
    
    ctk.CTkButton(frame_botoes, text="Atualizar Lista", 
                 command=atualizar_lista_alunos).pack(side="left", padx=5)
    ctk.CTkButton(frame_botoes, text="Novo Aluno", 
                 command=abrir_cadastro_aluno).pack(side="left", padx=5)

    # Carregar lista inicial
    atualizar_lista_alunos()

    # ====================================================
    # --- ABA PROFESSORES ---
    # ====================================================
    frame_prof = tabview.tab("Professores")

    # Seção de Lista
    colunas_prof = ('id', 'nome', 'sobrenome', 'email')
    larguras_prof = (50, 150, 150, 200)
    frame_lista_prof, tabela_prof = criar_secao_lista(frame_prof, "Lista de Professores", 
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
        
        criar_janela_cadastro(frame_prof, "Cadastrar Professor", 
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

    # ====================================================
    # --- ABA CURSOS ---
    # ====================================================
    frame_cursos = tabview.tab("Cursos")

    # Seção de Lista
    colunas_cursos = ('id', 'nome')
    larguras_cursos = (50, 400)
    frame_lista_cursos, tabela_cursos = criar_secao_lista(frame_cursos, "Lista de Cursos", 
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
        
        criar_janela_cadastro(frame_cursos, "Cadastrar Curso", 
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

    # ====================================================
    # --- ABA DISCIPLINAS ---
    # ====================================================
    frame_disciplinas = tabview.tab("Disciplinas")

    # Seção de Lista
    colunas_disciplinas = ('id', 'nome')
    larguras_disciplinas = (50, 400)
    frame_lista_disciplinas, tabela_disciplinas = criar_secao_lista(frame_disciplinas, 
                                                                   "Lista de Disciplinas", 
                                                                   colunas_disciplinas, 
                                                                   larguras_disciplinas)
    
    def atualizar_lista_disciplinas():
        response = listar_disciplinas()
        if response["status"] == "ok":
            tabela_disciplinas.clear()
            for disciplina in response["data"]:
                tabela_disciplinas.insert('', 'end', values=(
                    disciplina['id'],
                    disciplina['nome']
                ))

    def abrir_cadastro_disciplina():
        # Obter lista de professores e cursos
        response_profs = listar_professores()
        professores = response_profs["data"] if response_profs["status"] == "ok" else []
        
        response_cursos = listar_cursos()
        cursos = response_cursos["data"] if response_cursos["status"] == "ok" else []
        
        campos_disciplina = [
            {'name': 'nome', 'placeholder': 'Nome da Disciplina'},
            {'name': 'professor_id', 'type': 'select', 'label': 'Selecione o Professor:', 'options': professores},
            {'name': 'curso_id', 'type': 'select', 'label': 'Selecione o Curso:', 'options': cursos}
        ]
        
        def cadastrar_disciplina_handler(**kwargs):
            professor_id = kwargs.pop('professor_id', None)
            curso_id = kwargs.pop('curso_id', None)
            response = cadastrar_disciplina(kwargs['nome'])
            
            if response["status"] == "ok":
                disciplina_id = response["data"]["id"]
                # Associar professor e curso à disciplina
                if professor_id:
                    atribuir_professor_disciplina(professor_id, disciplina_id)
                if curso_id:
                    associar_disciplina_curso(disciplina_id, curso_id)
                atualizar_lista_disciplinas()
            return response
        
        criar_janela_cadastro(frame_disciplinas, "Cadastrar Disciplina", 
                            cadastrar_disciplina_handler, campos_disciplina)
    
    # Botões de ação
    frame_botoes = ctk.CTkFrame(frame_lista_disciplinas)
    frame_botoes.pack(fill="x", padx=5, pady=5)
    
    ctk.CTkButton(frame_botoes, text="Atualizar Lista", 
                 command=atualizar_lista_disciplinas).pack(side="left", padx=5)
    ctk.CTkButton(frame_botoes, text="Nova Disciplina", 
                 command=abrir_cadastro_disciplina).pack(side="left", padx=5)

    # Carregar lista inicial
    atualizar_lista_disciplinas()

    # ====================================================
    # --- ABA TURMAS ---
    # ====================================================
    frame_turmas = tabview.tab("Turmas")

    # Seção de Lista
    colunas_turmas = ('id', 'nome')
    larguras_turmas = (50, 400)
    frame_lista_turmas, tabela_turmas = criar_secao_lista(frame_turmas, "Lista de Turmas", 
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

    # def abrir_cadastro_turma():
        # Obter lista de cursos
        response_cursos = listar_cursos()
        cursos = response_cursos["data"] if response_cursos["status"] == "ok" else []
        
        # Função para atualizar disciplinas baseado no curso selecionado
        def atualizar_disciplinas(event=None):
            curso_selecionado = entries['curso'].get()
            if not curso_selecionado:
                entries['disciplinas'].configure(values=[])
                return
                
            curso_id = curso_selecionado.split(' - ')[0]
            response_disciplinas = listar_disciplinas()
            if response_disciplinas["status"] == "ok":
                disciplinas_todas = response_disciplinas["data"]
                # Aqui você precisaria de uma função no backend para filtrar as disciplinas por curso
                # Por enquanto, vamos mostrar todas as disciplinas
                entries['disciplinas'].configure(
                    values=[f"{d['id']} - {d['nome']}" for d in disciplinas_todas]
                )
        
        campos = [
            {'name': 'nome_turma', 'placeholder': 'Nome da Turma'},
            {
                'name': 'curso',
                'type': 'select',
                'placeholder': 'Selecione o Curso',
                'values': [f"{c['id']} - {c['nome']}" for c in cursos],
                'on_select': atualizar_disciplinas
            },
            {
                'name': 'disciplinas',
                'type': 'multiselect',
                'placeholder': 'Selecione as Disciplinas',
                'values': [],  # Será preenchido quando um curso for selecionado
            }
        ]
        
        def cadastrar_turma_handler(**kwargs):
            nome_turma = kwargs.get('nome_turma')
            curso = kwargs.get('curso')
            disciplinas = kwargs.get('disciplinas')
            
            curso_id = None
            if curso:
                curso_id = curso.split(' - ')[0]
                
            disciplinas_ids = []
            if disciplinas:
                # Para multiselect, disciplinas vem como uma lista de strings
                disciplinas_ids = [d.split(' - ')[0] for d in disciplinas]
                
            return criar_turma(
                nome_turma=nome_turma,
                curso_id=curso_id,
                disciplinas_ids=disciplinas_ids
            )

    def abrir_cadastro_turma():
        from .utils import MultiSelectComboBox
        
        # Obter lista de cursos
        response_cursos = listar_cursos()
        cursos = response_cursos["data"] if response_cursos["status"] == "ok" else []
        
        # Criar janela
        window = ctk.CTkToplevel(frame_turmas)
        window.title("Criar Nova Turma")
        window.geometry("400x600")
        window.transient(frame_turmas)
        window.grab_set()
        
        frame = ctk.CTkFrame(window)
        frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Título
        ctk.CTkLabel(frame, text="Criar Nova Turma", 
                    font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        
        # Nome da Turma
        frame_nome = ctk.CTkFrame(frame, fg_color="transparent")
        frame_nome.pack(fill="x", padx=5, pady=2)
        ctk.CTkLabel(frame_nome, text="Nome da Turma:").pack(anchor="w")
        entry_nome = ctk.CTkEntry(frame_nome)
        entry_nome.pack(fill="x", pady=5)
        
        # Curso
        frame_curso = ctk.CTkFrame(frame, fg_color="transparent")
        frame_curso.pack(fill="x", padx=5, pady=2)
        ctk.CTkLabel(frame_curso, text="Selecione o Curso:").pack(anchor="w")
        combo_curso = ctk.CTkComboBox(
            frame_curso,
            values=[f"{c['id']} - {c['nome']}" for c in cursos],
            state="readonly"
        )
        combo_curso.pack(fill="x", pady=5)
        
        # Disciplinas
        frame_disc = ctk.CTkFrame(frame, fg_color="transparent")
        frame_disc.pack(fill="x", padx=5, pady=2)
        ctk.CTkLabel(frame_disc, text="Selecione as Disciplinas:").pack(anchor="w")
        
        multiselect_disc = MultiSelectComboBox(frame_disc)
        multiselect_disc.pack(fill="x", pady=5)
        
        def atualizar_disciplinas(event=None):
            curso_selecionado = combo_curso.get()
            if not curso_selecionado:
                multiselect_disc.clear()
                return

            response_disciplinas = listar_disciplinas()
            if response_disciplinas["status"] == "ok":
                disciplinas_todas = response_disciplinas["data"]
                # Por enquanto, mostra todas as disciplinas
                # Idealmente, filtrar por curso no backend
                multiselect_disc.configure(
                    values=[f"{d['id']} - {d['nome']}" for d in disciplinas_todas]
                )
        
        combo_curso.configure(command=atualizar_disciplinas)
        
        def cadastrar():
            nome_turma = entry_nome.get()
            curso = combo_curso.get()
            disciplinas = multiselect_disc.get()
            
            curso_id = None
            if curso:
                curso_id = curso.split(' - ')[0]
                
            disciplinas_ids = []
            if disciplinas:
                disciplinas_ids = [d.split(' - ')[0] for d in disciplinas]
            
            response = criar_turma(
                nome_turma=nome_turma,
                curso_id=curso_id,
                disciplinas_ids=disciplinas_ids
            )
            
            if response["status"] == "ok":
                window.destroy()
                mostrar_feedback(frame_turmas, response["message"], "success")
                atualizar_lista_turmas()
            else:
                mostrar_feedback(frame, response["message"], "error")
        
        # Botões
        frame_botoes = ctk.CTkFrame(frame, fg_color="transparent")
        frame_botoes.pack(fill="x", pady=20)
        
        ctk.CTkButton(frame_botoes, text="Cadastrar", command=cadastrar).pack(pady=5)
        ctk.CTkButton(frame_botoes, text="Cancelar", command=window.destroy).pack(pady=5)
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    # Botões de ação
    frame_botoes = ctk.CTkFrame(frame_lista_turmas)
    frame_botoes.pack(fill="x", padx=5, pady=5)
    
    ctk.CTkButton(frame_botoes, text="Atualizar Lista", 
                 command=atualizar_lista_turmas).pack(side="left", padx=5)
    ctk.CTkButton(frame_botoes, text="Nova Turma", 
                 command=abrir_cadastro_turma).pack(side="left", padx=5)

    # Carregar lista inicial
    atualizar_lista_turmas()

    # ====================================================
    # --- ABA ATRIBUIÇÕES ---
    # ====================================================
    frame_atrib = tabview.tab("Atribuições")

    # Frame para Associar Disciplina-Curso
    frame_disc_curso = ctk.CTkFrame(frame_atrib)
    frame_disc_curso.pack(fill="x", padx=10, pady=5)
    
    ctk.CTkLabel(frame_disc_curso, text="Associar Disciplina ao Curso:").pack(pady=5)
    
    entry_id_disc = ctk.CTkEntry(frame_disc_curso, placeholder_text="ID da Disciplina")
    entry_id_disc.pack(fill="x", padx=5, pady=2)
    
    entry_id_curso = ctk.CTkEntry(frame_disc_curso, placeholder_text="ID do Curso")
    entry_id_curso.pack(fill="x", padx=5, pady=2)

    def associar_disc_curso_handler():
        response = associar_disciplina_curso(entry_id_disc.get(), entry_id_curso.get())
        processar_resposta(response, frame_disc_curso, [entry_id_disc, entry_id_curso])

    btn_associar_disc_curso = ctk.CTkButton(
        frame_disc_curso,
        text="Associar",
        command=associar_disc_curso_handler
    )
    btn_associar_disc_curso.pack(pady=10)

    # Frame para Atribuir Professor-Disciplina
    frame_prof_disc = ctk.CTkFrame(frame_atrib)
    frame_prof_disc.pack(fill="x", padx=10, pady=5)
    
    ctk.CTkLabel(frame_prof_disc, text="Atribuir Professor à Disciplina:").pack(pady=5)
    
    entry_id_prof = ctk.CTkEntry(frame_prof_disc, placeholder_text="ID do Professor")
    entry_id_prof.pack(fill="x", padx=5, pady=2)
    
    entry_id_disc_prof = ctk.CTkEntry(frame_prof_disc, placeholder_text="ID da Disciplina")
    entry_id_disc_prof.pack(fill="x", padx=5, pady=2)

    def atribuir_prof_disc_handler():
        response = atribuir_professor_disciplina(entry_id_prof.get(), entry_id_disc_prof.get())
        processar_resposta(response, frame_prof_disc, [entry_id_prof, entry_id_disc_prof])

    btn_atribuir_prof_disc = ctk.CTkButton(
        frame_prof_disc,
        text="Atribuir",
        command=atribuir_prof_disc_handler
    )
    btn_atribuir_prof_disc.pack(pady=10)

    # Frame para Associar Turma-Curso
    frame_turma_curso = ctk.CTkFrame(frame_atrib)
    frame_turma_curso.pack(fill="x", padx=10, pady=5)
    
    ctk.CTkLabel(frame_turma_curso, text="Associar Turma ao Curso:").pack(pady=5)
    
    entry_id_turma_curso = ctk.CTkEntry(frame_turma_curso, placeholder_text="ID da Turma")
    entry_id_turma_curso.pack(fill="x", padx=5, pady=2)
    
    entry_id_curso_turma = ctk.CTkEntry(frame_turma_curso, placeholder_text="ID do Curso")
    entry_id_curso_turma.pack(fill="x", padx=5, pady=2)

    def associar_turma_curso_handler():
        response = associar_turma_curso(entry_id_turma_curso.get(), entry_id_curso_turma.get())
        processar_resposta(response, frame_turma_curso, [entry_id_turma_curso, entry_id_curso_turma])

    btn_associar_turma_curso = ctk.CTkButton(
        frame_turma_curso,
        text="Associar",
        command=associar_turma_curso_handler
    )
    btn_associar_turma_curso.pack(pady=10)

    # Frame para Atribuir Aluno-Turma
    frame_aluno_turma = ctk.CTkFrame(frame_atrib)
    frame_aluno_turma.pack(fill="x", padx=10, pady=5)
    
    ctk.CTkLabel(frame_aluno_turma, text="Atribuir Aluno à Turma:").pack(pady=5)
    
    entry_id_aluno = ctk.CTkEntry(frame_aluno_turma, placeholder_text="ID do Aluno")
    entry_id_aluno.pack(fill="x", padx=5, pady=2)
    
    entry_id_turma_aluno = ctk.CTkEntry(frame_aluno_turma, placeholder_text="ID da Turma")
    entry_id_turma_aluno.pack(fill="x", padx=5, pady=2)

    def atribuir_aluno_turma_handler():
        response = atribuir_aluno_turma(entry_id_aluno.get(), entry_id_turma_aluno.get())
        processar_resposta(response, frame_aluno_turma, [entry_id_aluno, entry_id_turma_aluno])

    btn_atribuir_aluno_turma = ctk.CTkButton(
        frame_aluno_turma,
        text="Atribuir",
        command=atribuir_aluno_turma_handler
    )
    btn_atribuir_aluno_turma.pack(pady=10)
