import customtkinter as ctk
from ..components.list_section import criar_secao_lista
from ..components.cadastro_dialog import criar_janela_cadastro
from controller import criar_turma, listar_turmas, listar_cursos, listar_disciplinas

def create_class_tab(tab):
    # Seção de Lista
    colunas_turmas = ('id', 'nome')
    larguras_turmas = (50, 400)
    frame_lista_turmas, tabela_turmas = criar_secao_lista(tab, "Lista de Turmas", 
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

    def abrir_cadastro_turma():
        from ...utils import MultiSelectComboBox
        
        # Obter lista de cursos
        response_cursos = listar_cursos()
        cursos = response_cursos["data"] if response_cursos["status"] == "ok" else []
        
        # Criar janela
        window = ctk.CTkToplevel(frame_lista_turmas)
        window.title("Criar Nova Turma")
        window.geometry("400x600")
        window.transient(frame_lista_turmas)
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
                atualizar_lista_turmas()
        
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

    return frame_lista_turmas