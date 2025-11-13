import customtkinter as ctk

class DisciplineCard(ctk.CTkFrame):
    """Card visual para exibir informações de uma disciplina"""
    
    def __init__(self, parent, disciplina, on_click=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.disciplina = disciplina
        self.on_click = on_click
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura a interface do card"""
        
        # Container principal com padding
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Header com nome da disciplina
        header_frame = ctk.CTkFrame(main_frame, height=50, corner_radius=8,
                                   fg_color=("#f0f0f0", "#2b2b2b"))
        header_frame.pack(fill="x", pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Nome da disciplina
        nome_label = ctk.CTkLabel(
            header_frame,
            text=self.disciplina.get('nome', 'Disciplina sem nome'),
            font=ctk.CTkFont(size=16, weight="bold"),
            wraplength=300
        )
        nome_label.pack(pady=15)
        
        # Informações do curso
        curso_label = ctk.CTkLabel(
            main_frame,
            text=f"📚 {self.disciplina.get('curso_nome', 'Curso não informado')}",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        curso_label.pack(anchor="w", pady=(0, 5))
        
        # Progresso
        progresso = self.disciplina.get('progresso', {})
        total_aulas = progresso.get('total_aulas', 0)
        aulas_concluidas = progresso.get('aulas_concluidas', 0)
        percentual = progresso.get('percentual', 0)
        
        # Frame do progresso
        progress_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        progress_frame.pack(fill="x", pady=5)
        
        # Texto do progresso
        progresso_text = f"📊 Progresso: {aulas_concluidas}/{total_aulas} aulas ({percentual}%)"
        progresso_label = ctk.CTkLabel(
            progress_frame,
            text=progresso_text,
            font=ctk.CTkFont(size=11)
        )
        progresso_label.pack(anchor="w")
        
        # Barra de progresso
        progress_bar = ctk.CTkProgressBar(progress_frame, height=8)
        progress_bar.pack(fill="x", pady=(5, 0))
        progress_bar.set(percentual / 100 if total_aulas > 0 else 0)
        
        # Status badge
        status_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        status_frame.pack(fill="x", pady=(10, 5))
        
        if percentual >= 100:
            status_color = "green"
            status_text = "✅ Concluída"
        elif percentual > 0:
            status_color = "orange"
            status_text = "🟡 Em andamento"
        else:
            status_color = "gray"
            status_text = "⚪ Não iniciada"
            
        status_label = ctk.CTkLabel(
            status_frame,
            text=status_text,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=status_color
        )
        status_label.pack(anchor="w")
        
        # Botão de ação
        action_btn = ctk.CTkButton(
            main_frame,
            text="📖 Acessar Disciplina",
            command=self._on_card_click,
            height=35,
            corner_radius=8
        )
        action_btn.pack(fill="x", pady=(15, 5))
        
        # Torna o card clicável
        self.configure(cursor="hand2")
        self.bind("<Button-1>", lambda e: self._on_card_click())
        
    def _on_card_click(self):
        """Manipula o clique no card"""
        if self.on_click:
            self.on_click(self.disciplina)