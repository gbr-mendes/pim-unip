import customtkinter as ctk

class SearchAndFilterWidget(ctk.CTkFrame):
    """Widget para busca e filtro de disciplinas"""
    
    def __init__(self, parent, on_search_change=None, on_filter_change=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.on_search_change = on_search_change
        self.on_filter_change = on_filter_change
        
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
            text="🔍 Buscar e Filtrar",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left")
        
        # Controles
        controls_frame = ctk.CTkFrame(main_frame)
        controls_frame.pack(fill="x", pady=5, padx=10)
        
        # Busca
        search_frame = ctk.CTkFrame(controls_frame)
        search_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(search_frame, text="Buscar:", font=ctk.CTkFont(size=12)).pack(side="left", padx=(5, 10))
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Nome da disciplina...",
            width=200
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.search_entry.bind("<KeyRelease>", self._on_search_change)
        
        # Filtro por curso
        filter_frame = ctk.CTkFrame(controls_frame)
        filter_frame.pack(side="right")
        
        ctk.CTkLabel(filter_frame, text="Curso:", font=ctk.CTkFont(size=12)).pack(side="left", padx=(5, 10))
        
        self.course_filter = ctk.CTkOptionMenu(
            filter_frame,
            values=["Todos os cursos"],
            width=200,
            command=self._on_filter_change
        )
        self.course_filter.pack(side="right", padx=(0, 5))
        
    def _on_search_change(self, event=None):
        """Callback para mudança na busca"""
        if self.on_search_change:
            search_text = self.search_entry.get().strip()
            self.on_search_change(search_text)
            
    def _on_filter_change(self, value):
        """Callback para mudança no filtro"""
        if self.on_filter_change:
            self.on_filter_change(value)
            
    def update_course_options(self, courses):
        """Atualiza as opções de curso no filtro"""
        course_names = ["Todos os cursos"] + [curso['nome'] for curso in courses]
        self.course_filter.configure(values=course_names)
        self.course_filter.set("Todos os cursos")
        
    def get_search_text(self):
        """Retorna o texto de busca atual"""
        return self.search_entry.get().strip()
        
    def get_selected_course(self):
        """Retorna o curso selecionado no filtro"""
        return self.course_filter.get()
        
    def clear_search(self):
        """Limpa o campo de busca"""
        self.search_entry.delete(0, 'end')