import customtkinter as ctk

class StatsWidget(ctk.CTkFrame):
    """Widget para exibir estatísticas rápidas do professor"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.stats = {
            'total_disciplinas': 0,
            'total_cursos': 0
        }
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Configura a interface do widget"""
        # Frame principal
        main_frame = ctk.CTkFrame(self, corner_radius=10)
        main_frame.pack(fill="x", pady=5, padx=5)
        
        # Título
        title_frame = ctk.CTkFrame(main_frame)
        title_frame.pack(fill="x", pady=5, padx=10)
        
        ctk.CTkLabel(
            title_frame,
            text="📊 Resumo Rápido",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left")
        
        # Container das estatísticas
        stats_container = ctk.CTkFrame(main_frame)
        stats_container.pack(fill="x", pady=5, padx=10)
        
        # Cards de estatísticas
        self.disciplinas_card = self._create_stat_card(
            stats_container, "📖", "Disciplinas", "0", "Total de disciplinas"
        )
        self.disciplinas_card.pack(side="left", fill="x", expand=True, padx=5)
        
        self.cursos_card = self._create_stat_card(
            stats_container, "📚", "Cursos", "0", "Cursos diferentes"
        )
        self.cursos_card.pack(side="left", fill="x", expand=True, padx=5)
        
    def _create_stat_card(self, parent, icon, title, value, subtitle):
        """Cria um card de estatística"""
        card = ctk.CTkFrame(parent, corner_radius=8)
        
        # Ícone
        icon_label = ctk.CTkLabel(
            card,
            text=icon,
            font=ctk.CTkFont(size=20)
        )
        icon_label.pack(pady=(10, 5))
        
        # Valor
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=24, weight="bold")
        )
        value_label.pack()
        
        # Título
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        title_label.pack()
        
        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            card,
            text=subtitle,
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        subtitle_label.pack(pady=(0, 10))
        
        # Armazena referências para atualização
        card.value_label = value_label
        card.title_label = title_label
        
        return card
        
    def update_stats(self, disciplinas, cursos):
        """Atualiza as estatísticas baseado nos dados fornecidos"""
        # Total de disciplinas
        total_disciplinas = len(disciplinas)
        self.disciplinas_card.value_label.configure(text=str(total_disciplinas))
        
        # Total de cursos únicos
        cursos_ids = set(d.get('curso_id') for d in disciplinas if d.get('curso_id'))
        total_cursos = len(cursos_ids)
        self.cursos_card.value_label.configure(text=str(total_cursos))
            
        # Atualiza estatísticas internas
        self.stats = {
            'total_disciplinas': total_disciplinas,
            'total_cursos': total_cursos
        }
        
    def get_stats(self):
        """Retorna as estatísticas atuais"""
        return self.stats.copy()