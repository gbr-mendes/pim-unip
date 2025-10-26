import customtkinter as ctk

class DisciplineCard(ctk.CTkFrame):
    """Card clicável para exibir informações de uma disciplina"""
    
    def __init__(self, parent, disciplina, curso_nome, on_click=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.disciplina = disciplina
        self.curso_nome = curso_nome
        self.on_click = on_click
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Configura a interface do card"""
        # Frame principal com padding
        main_frame = ctk.CTkFrame(self, corner_radius=10)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Header com ícone e nome da disciplina
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", pady=5, padx=10)
        
        # Ícone da disciplina
        icon_label = ctk.CTkLabel(header_frame, text="📖", font=ctk.CTkFont(size=20))
        icon_label.pack(side="left", padx=(5, 10))
        
        # Nome da disciplina
        nome_label = ctk.CTkLabel(
            header_frame, 
            text=self.disciplina['nome'],
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        nome_label.pack(side="left", fill="x", expand=True)
        
        # Info frame
        info_frame = ctk.CTkFrame(main_frame)
        info_frame.pack(fill="x", pady=5, padx=10)
        
        # ID da disciplina
        id_label = ctk.CTkLabel(
            info_frame,
            text=f"ID: {self.disciplina['id']}",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        id_label.pack(side="left", padx=5)
        
        # Nome do curso
        curso_label = ctk.CTkLabel(
            info_frame,
            text=f"Curso: {self.curso_nome}",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        curso_label.pack(side="right", padx=5)
        
        # Botão de ação
        action_frame = ctk.CTkFrame(main_frame)
        action_frame.pack(fill="x", pady=5, padx=10)
        
        gerenciar_btn = ctk.CTkButton(
            action_frame,
            text="📋 Gerenciar Disciplina",
            font=ctk.CTkFont(size=12),
            height=35,
            command=self._handle_click,
            fg_color=("gray70", "gray25"),
            hover_color=("gray65", "gray30")
        )
        gerenciar_btn.pack(fill="x", pady=5)
        
        # Efeito hover no card completo
        self._bind_hover_effect(main_frame)
        
    def _handle_click(self):
        """Manipula o clique no card"""
        if self.on_click:
            self.on_click(self.disciplina)
            
    def _bind_hover_effect(self, widget):
        """Adiciona efeito de hover ao card"""
        def on_enter(event):
            widget.configure(fg_color=("gray75", "gray20"))
            
        def on_leave(event):
            widget.configure(fg_color=("gray78", "gray17"))
            
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

class CourseSection(ctk.CTkFrame):
    """Seção que agrupa disciplinas de um curso"""
    
    def __init__(self, parent, curso, disciplinas, on_disciplina_click=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.curso = curso
        self.disciplinas = disciplinas
        self.on_disciplina_click = on_disciplina_click
        self.is_expanded = True
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Configura a interface da seção"""
        # Header do curso
        self.header_frame = ctk.CTkFrame(self, corner_radius=10)
        self.header_frame.pack(fill="x", pady=5, padx=5)
        
        # Botão para expandir/colapsar
        self.toggle_btn = ctk.CTkButton(
            self.header_frame,
            text="▼",
            width=30,
            height=30,
            font=ctk.CTkFont(size=12),
            command=self._toggle_expand,
            fg_color="transparent",
            hover_color=("gray75", "gray25")
        )
        self.toggle_btn.pack(side="left", padx=5)
        
        # Ícone e nome do curso
        ctk.CTkLabel(
            self.header_frame,
            text="📚",
            font=ctk.CTkFont(size=18)
        ).pack(side="left", padx=(5, 10))
        
        ctk.CTkLabel(
            self.header_frame,
            text=self.curso['nome'],
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        ).pack(side="left", fill="x", expand=True)
        
        # Contador de disciplinas
        ctk.CTkLabel(
            self.header_frame,
            text=f"{len(self.disciplinas)} disciplina(s)",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(side="right", padx=10)
        
        # Container das disciplinas
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(fill="both", expand=True, pady=5, padx=5)
        
        # Adiciona os cards das disciplinas
        self._create_discipline_cards()
        
    def _create_discipline_cards(self):
        """Cria os cards das disciplinas"""
        for disciplina in self.disciplinas:
            card = DisciplineCard(
                self.content_frame,
                disciplina,
                self.curso['nome'],
                on_click=self.on_disciplina_click,
                corner_radius=8
            )
            card.pack(fill="x", pady=3, padx=5)
            
    def _toggle_expand(self):
        """Alterna entre expandido e colapsado"""
        self.is_expanded = not self.is_expanded
        
        if self.is_expanded:
            self.content_frame.pack(fill="both", expand=True, pady=5, padx=5)
            self.toggle_btn.configure(text="▼")
        else:
            self.content_frame.pack_forget()
            self.toggle_btn.configure(text="▶")

class EmptyState(ctk.CTkFrame):
    """Componente para exibir estado vazio"""
    
    def __init__(self, parent, message="Nenhum item encontrado", icon="📝", **kwargs):
        super().__init__(parent, **kwargs)
        
        self.message = message
        self.icon = icon
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Configura a interface do estado vazio"""
        # Frame central
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(expand=True, fill="both")
        
        # Ícone
        icon_label = ctk.CTkLabel(
            content_frame,
            text=self.icon,
            font=ctk.CTkFont(size=48)
        )
        icon_label.pack(pady=(50, 20))
        
        # Mensagem
        message_label = ctk.CTkLabel(
            content_frame,
            text=self.message,
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        message_label.pack(pady=10)