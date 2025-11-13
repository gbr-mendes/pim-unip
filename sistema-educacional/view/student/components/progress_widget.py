import customtkinter as ctk

class ProgressWidget(ctk.CTkFrame):
    """Widget para exibir estatísticas de progresso do aluno"""
    
    def __init__(self, parent, height=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.custom_height = height
        self.setup_ui()
        
    def setup_ui(self):
        """Configura a interface do widget"""
        
        # Se é versão compacta, usar layout horizontal
        is_compact = self.custom_height and self.custom_height <= 80
        
        if is_compact:
            # Layout horizontal compacto
            main_frame = ctk.CTkFrame(self, fg_color="transparent")
            main_frame.pack(fill="both", expand=True, padx=10, pady=5)
            
            # Título compacto à esquerda
            titulo = ctk.CTkLabel(
                main_frame,
                text="📊 Progresso",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            titulo.pack(side="left", padx=(0, 20))
            
            # Container para estatísticas horizontais
            self.stats_container = ctk.CTkFrame(main_frame, fg_color="transparent")
            self.stats_container.pack(side="left", fill="x", expand=True)
        else:
            # Layout vertical padrão
            # Título
            titulo = ctk.CTkLabel(
                self,
                text="📊 Seu Progresso Acadêmico",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            titulo.pack(pady=(15, 10))
            
            # Container para estatísticas
            self.stats_container = ctk.CTkFrame(self, fg_color="transparent")
            self.stats_container.pack(fill="x", padx=20, pady=(0, 15))
        
        # Placeholder inicial
        self.loading_label = ctk.CTkLabel(
            self.stats_container,
            text="🔄 Carregando...",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.loading_label.pack(pady=10)
        
    def update_stats(self, stats):
        """Atualiza as estatísticas exibidas"""
        
        # Remove widgets anteriores
        for widget in self.stats_container.winfo_children():
            widget.destroy()
            
        # Verifica se é layout compacto
        is_compact = self.custom_height and self.custom_height <= 80
        
        # Dados das estatísticas
        total_aulas = stats.get('total_aulas', 0)
        aulas_concluidas = stats.get('aulas_concluidas', 0)
        aulas_pendentes = stats.get('aulas_pendentes', 0)
        percentual = stats.get('percentual_conclusao', 0)
        disciplinas = stats.get('disciplinas_matriculadas', 0)
        
        if is_compact:
            # Layout horizontal compacto com mais espaço
            stats_data = [
                ("🎓", f"{disciplinas}", "Disciplinas"),
                ("📚", f"{total_aulas}", "Aulas"),
                ("✅", f"{aulas_concluidas}", "OK"),
                ("📈", f"{percentual:.0f}%", "Completo")
            ]
            
            for i, (icon, valor, label) in enumerate(stats_data):
                stat_frame = ctk.CTkFrame(self.stats_container, width=100, height=40)
                stat_frame.pack(side="left", padx=3, fill="y")
                stat_frame.pack_propagate(False)
                
                # Container principal
                content_frame = ctk.CTkFrame(stat_frame, fg_color="transparent")
                content_frame.pack(expand=True, fill="both", padx=2, pady=2)
                
                # Linha superior: ícone e valor
                top_frame = ctk.CTkFrame(content_frame, fg_color="transparent", height=20)
                top_frame.pack(fill="x")
                top_frame.pack_propagate(False)
                
                icon_label = ctk.CTkLabel(top_frame, text=icon, font=ctk.CTkFont(size=12))
                icon_label.pack(side="left", padx=(3, 2))
                
                valor_label = ctk.CTkLabel(top_frame, text=valor, font=ctk.CTkFont(size=12, weight="bold"))
                valor_label.pack(side="left")
                
                # Linha inferior: descrição
                desc_label = ctk.CTkLabel(content_frame, text=label, font=ctk.CTkFont(size=9), text_color="gray")
                desc_label.pack(pady=(0, 2))
        else:
            # Layout vertical padrão (grid)
            grid_frame = ctk.CTkFrame(self.stats_container, fg_color="transparent")
            grid_frame.pack(fill="x", pady=10)
            
            # Dados das estatísticas para layout vertical
            stats_data = [
                ("📚", f"{total_aulas}", "Total de Aulas"),
                ("✅", f"{aulas_concluidas}", "Concluídas"),
                ("⏳", f"{aulas_pendentes}", "Pendentes"),
                ("📊", f"{percentual:.1f}%", "Progresso"),
                ("🎓", f"{disciplinas}", "Disciplinas")
            ]
            
            # Cria grid 5x1
            for i, (icon, valor, descricao) in enumerate(stats_data):
                self.create_stat_card(grid_frame, icon, valor, descricao, i)
            
            # Configura grid
            for i in range(5):
                grid_frame.grid_columnconfigure(i, weight=1)
            
            # Barra de progresso
            if total_aulas > 0:
                progress_frame = ctk.CTkFrame(self.stats_container, fg_color="transparent")
                progress_frame.pack(fill="x", pady=(10, 0))
                
                progress_label = ctk.CTkLabel(
                    progress_frame,
                    text=f"Progresso Geral: {percentual:.1f}%",
                    font=ctk.CTkFont(size=12, weight="bold")
                )
                progress_label.pack()
                
                progress_bar = ctk.CTkProgressBar(progress_frame, width=400)
                progress_bar.pack(pady=(5, 0))
                progress_bar.set(percentual / 100)
        

            
    def _create_stat_card(self, parent, card_data):
        """Cria um card individual de estatística"""
        
        card = ctk.CTkFrame(parent, corner_radius=8)
        
        # Ícone e título
        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.pack(pady=10)
        
        icon_label = ctk.CTkLabel(
            header_frame,
            text=card_data["icon"],
            font=ctk.CTkFont(size=20)
        )
        icon_label.pack()
        
        title_label = ctk.CTkLabel(
            header_frame,
            text=card_data["title"],
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        title_label.pack()
        
        # Valor
        value_label = ctk.CTkLabel(
            card,
            text=card_data["value"],
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=card_data["color"]
        )
        value_label.pack(pady=(0, 15))
        
        return card