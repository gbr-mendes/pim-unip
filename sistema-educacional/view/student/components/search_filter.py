import customtkinter as ctk

class StudentSearchFilter(ctk.CTkFrame):
    """Widget de busca e filtros para o dashboard do aluno"""
    
    def __init__(self, parent, on_search_change=None, on_filter_change=None, on_buscar_conteudo=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.on_search_change = on_search_change
        self.on_filter_change = on_filter_change
        self.on_buscar_conteudo = on_buscar_conteudo
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura a interface do widget"""
        
        # Container principal
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="x", padx=15, pady=15)
        
        # Linha superior - busca por disciplinas
        search_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, 10))
        
        # Label de busca
        search_label = ctk.CTkLabel(
            search_frame,
            text="🔍 Buscar disciplinas:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        search_label.pack(side="left", padx=(0, 10))
        
        # Campo de busca
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Digite o nome da disciplina ou curso...",
            height=35,
            width=300
        )
        self.search_entry.pack(side="left", padx=(0, 15))
        self.search_entry.bind("<KeyRelease>", self._on_search_change)
        
        # Filtro de progresso
        filter_label = ctk.CTkLabel(
            search_frame,
            text="📊 Filtrar por:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        filter_label.pack(side="left", padx=(0, 10))
        
        self.filter_combo = ctk.CTkComboBox(
            search_frame,
            values=["Todas", "Concluídas", "Em andamento", "Não iniciadas"],
            command=self._on_filter_change,
            height=35,
            width=150
        )
        self.filter_combo.pack(side="left")
        self.filter_combo.set("Todas")
        
        # Linha inferior - busca global de conteúdo
        content_search_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_search_frame.pack(fill="x", pady=(10, 0))
        
        # Label de busca de conteúdo
        content_label = ctk.CTkLabel(
            content_search_frame,
            text="🔎 Buscar conteúdo nas aulas:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        content_label.pack(side="left", padx=(0, 10))
        
        # Campo de busca de conteúdo
        self.content_entry = ctk.CTkEntry(
            content_search_frame,
            placeholder_text="Buscar em módulos e aulas...",
            height=35,
            width=300
        )
        self.content_entry.pack(side="left", padx=(0, 10))
        self.content_entry.bind("<Return>", self._on_content_search)
        
        # Botão de busca de conteúdo
        search_btn = ctk.CTkButton(
            content_search_frame,
            text="Buscar",
            command=self._on_content_search,
            height=35,
            width=80
        )
        search_btn.pack(side="left")
        
    def _on_search_change(self, event=None):
        """Manipula mudanças no campo de busca"""
        if self.on_search_change:
            self.on_search_change(self.search_entry.get())
            
    def _on_filter_change(self, value):
        """Manipula mudanças no filtro"""
        if self.on_filter_change:
            self.on_filter_change(value)
            
    def _on_content_search(self, event=None):
        """Manipula busca de conteúdo"""
        if self.on_buscar_conteudo:
            termo = self.content_entry.get().strip()
            if termo:
                self.on_buscar_conteudo(termo)
                
    def get_search_text(self):
        """Retorna o texto atual da busca"""
        return self.search_entry.get()
        
    def get_selected_filter(self):
        """Retorna o filtro selecionado"""
        return self.filter_combo.get()
        
    def clear_search(self):
        """Limpa os campos de busca"""
        self.search_entry.delete(0, "end")
        self.content_entry.delete(0, "end")
        self.filter_combo.set("Todas")