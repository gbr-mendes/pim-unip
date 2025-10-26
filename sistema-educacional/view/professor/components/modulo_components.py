import customtkinter as ctk
from controller.aula_controller import listar_aulas_modulo

class ModuloCard(ctk.CTkFrame):
    """Card para exibir um módulo com suas aulas"""
    
    def __init__(self, parent, modulo, on_add_aula=None, on_edit_modulo=None, 
                 on_delete_modulo=None, on_preview_aula=None, on_edit_aula=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.modulo = modulo
        self.on_add_aula = on_add_aula
        self.on_edit_modulo = on_edit_modulo
        self.on_delete_modulo = on_delete_modulo
        self.on_preview_aula = on_preview_aula
        self.on_edit_aula = on_edit_aula
        self.is_expanded = True
        self.aulas = []
        
        self._setup_ui()
        self._load_aulas()
        
    def _setup_ui(self):
        """Configura a interface do card"""
        # Header do módulo
        self.header_frame = ctk.CTkFrame(self, corner_radius=10)
        self.header_frame.pack(fill="x", pady=5, padx=5)
        
        # Linha superior do header
        header_top = ctk.CTkFrame(self.header_frame)
        header_top.pack(fill="x", pady=10, padx=10)
        
        # Botão expandir/colapsar
        self.toggle_btn = ctk.CTkButton(
            header_top,
            text="▼",
            width=30,
            height=30,
            font=ctk.CTkFont(size=12),
            command=self._toggle_expand,
            fg_color="transparent",
            hover_color=("gray75", "gray25")
        )
        self.toggle_btn.pack(side="left", padx=(0, 10))
        
        # Info do módulo
        info_frame = ctk.CTkFrame(header_top)
        info_frame.pack(side="left", fill="x", expand=True)
        
        # Nome do módulo
        nome_label = ctk.CTkLabel(
            info_frame,
            text=f"📂 {self.modulo['nome']}",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        nome_label.pack(fill="x", padx=5)
        
        # Descrição (se houver)
        if self.modulo.get('descricao'):
            desc_label = ctk.CTkLabel(
                info_frame,
                text=self.modulo['descricao'],
                font=ctk.CTkFont(size=12),
                text_color="gray",
                anchor="w"
            )
            desc_label.pack(fill="x", padx=5)
        
        # Botões de ação
        actions_frame = ctk.CTkFrame(header_top)
        actions_frame.pack(side="right", padx=10)
        
        # Botão adicionar aula
        add_aula_btn = ctk.CTkButton(
            actions_frame,
            text="➕ Aula",
            width=80,
            height=30,
            command=self._add_aula,
            fg_color="green",
            hover_color="darkgreen"
        )
        add_aula_btn.pack(side="left", padx=2)
        
        # Botão editar módulo
        edit_btn = ctk.CTkButton(
            actions_frame,
            text="✏️",
            width=30,
            height=30,
            command=self._edit_modulo,
            fg_color="orange",
            hover_color="darkorange"
        )
        edit_btn.pack(side="left", padx=2)
        
        # Botão excluir módulo
        delete_btn = ctk.CTkButton(
            actions_frame,
            text="🗑️",
            width=30,
            height=30,
            command=self._delete_modulo,
            fg_color="red",
            hover_color="darkred"
        )
        delete_btn.pack(side="left", padx=2)
        
        # Container das aulas
        self.aulas_container = ctk.CTkFrame(self)
        self.aulas_container.pack(fill="x", pady=5, padx=5)
        
        # Label contador de aulas
        self.aulas_count_label = ctk.CTkLabel(
            self.header_frame,
            text="Carregando aulas...",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        self.aulas_count_label.pack(pady=5)
        
    def _load_aulas(self):
        """Carrega as aulas do módulo"""
        try:
            response = listar_aulas_modulo(self.modulo['id'])
            if response.get("status") == "ok":
                self.aulas = response.get("data", [])
                self._update_aulas_display()
            else:
                self.aulas_count_label.configure(text="Erro ao carregar aulas")
        except Exception as e:
            self.aulas_count_label.configure(text=f"Erro: {str(e)}")
            
    def _update_aulas_display(self):
        """Atualiza a exibição das aulas"""
        # Limpa container
        for widget in self.aulas_container.winfo_children():
            widget.destroy()
            
        # Atualiza contador
        count = len(self.aulas)
        self.aulas_count_label.configure(text=f"{count} aula(s)")
        
        if not self.aulas:
            empty_label = ctk.CTkLabel(
                self.aulas_container,
                text="Nenhuma aula criada ainda",
                font=ctk.CTkFont(size=12),
                text_color="gray"
            )
            empty_label.pack(pady=20)
        else:
            # Cria cards das aulas
            for aula in sorted(self.aulas, key=lambda a: a.get('ordem', 0)):
                aula_card = AulaCard(
                    self.aulas_container,
                    aula,
                    on_preview=self.on_preview_aula,
                    on_edit=self.on_edit_aula
                )
                aula_card.pack(fill="x", pady=2, padx=10)
                
    def _toggle_expand(self):
        """Alterna expansão do módulo"""
        self.is_expanded = not self.is_expanded
        
        if self.is_expanded:
            self.aulas_container.pack(fill="x", pady=5, padx=5)
            self.toggle_btn.configure(text="▼")
        else:
            self.aulas_container.pack_forget()
            self.toggle_btn.configure(text="▶")
            
    def _add_aula(self):
        """Chama callback para adicionar aula"""
        if self.on_add_aula:
            self.on_add_aula()
            
    def _edit_modulo(self):
        """Chama callback para editar módulo"""
        if self.on_edit_modulo:
            self.on_edit_modulo()
            
    def _delete_modulo(self):
        """Chama callback para excluir módulo"""
        if self.on_delete_modulo:
            self.on_delete_modulo()
            
    def refresh(self):
        """Recarrega as aulas"""
        self._load_aulas()

class AulaCard(ctk.CTkFrame):
    """Card para exibir uma aula"""
    
    def __init__(self, parent, aula, on_preview=None, on_edit=None, on_delete=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.aula = aula
        self.on_preview = on_preview
        self.on_edit = on_edit
        self.on_delete = on_delete
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Configura a interface do card"""
        # Frame principal
        main_frame = ctk.CTkFrame(self, corner_radius=8)
        main_frame.pack(fill="x", pady=2, padx=2)
        
        # Conteúdo
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(fill="x", pady=5, padx=10)
        
        # Info da aula
        info_frame = ctk.CTkFrame(content_frame)
        info_frame.pack(side="left", fill="x", expand=True)
        
        # Título
        titulo_label = ctk.CTkLabel(
            info_frame,
            text=f"🎥 {self.aula['titulo']}",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        titulo_label.pack(fill="x")
        
        # Resumo (primeira linha)
        resumo = self.aula.get('resumo', '')
        if resumo:
            resumo_preview = resumo.split('\n')[0][:50]
            if len(resumo_preview) < len(resumo):
                resumo_preview += "..."
                
            resumo_label = ctk.CTkLabel(
                info_frame,
                text=resumo_preview,
                font=ctk.CTkFont(size=10),
                text_color="gray",
                anchor="w"
            )
            resumo_label.pack(fill="x")
        
        # Indicador de vídeo
        if self.aula.get('video_url'):
            video_label = ctk.CTkLabel(
                info_frame,
                text="📹 Vídeo disponível",
                font=ctk.CTkFont(size=10),
                text_color="blue",
                anchor="w"
            )
            video_label.pack(fill="x")
        
        # Botões de ação
        actions_frame = ctk.CTkFrame(content_frame)
        actions_frame.pack(side="right", padx=10)
        
        # Botão preview
        preview_btn = ctk.CTkButton(
            actions_frame,
            text="👁️ Preview",
            width=80,
            height=30,
            command=self._preview,
            fg_color="blue",
            hover_color="darkblue"
        )
        preview_btn.pack(side="left", padx=2)
        
        # Botão editar (se callback fornecido)
        if self.on_edit:
            edit_btn = ctk.CTkButton(
                actions_frame,
                text="✏️",
                width=30,
                height=30,
                command=self._edit,
                fg_color="orange",
                hover_color="darkorange"
            )
            edit_btn.pack(side="left", padx=2)
        
        # Botão excluir (se callback fornecido)
        if self.on_delete:
            delete_btn = ctk.CTkButton(
                actions_frame,
                text="🗑️",
                width=30,
                height=30,
                command=self._delete,
                fg_color="red",
                hover_color="darkred"
            )
            delete_btn.pack(side="left", padx=2)
            
    def _preview(self):
        """Chama callback para preview"""
        if self.on_preview:
            self.on_preview(self.aula)
            
    def _edit(self):
        """Chama callback para editar"""
        if self.on_edit:
            self.on_edit(self.aula)
            
    def _delete(self):
        """Chama callback para excluir"""
        if self.on_delete:
            self.on_delete(self.aula)