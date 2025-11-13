import customtkinter as ctk
from controller.modulo_controller import listar_modulos_disciplina
from controller.aula_controller import listar_aulas_modulo
from controller.aluno_controller import obter_progresso_aluno, marcar_aula_concluida

class ModuleViewer(ctk.CTkToplevel):
    """Janela para visualização de módulos e aulas de uma disciplina"""
    
    def __init__(self, parent, disciplina, aluno_id):
        super().__init__(parent)
        
        self.disciplina = disciplina
        self.aluno_id = aluno_id
        self.modulos = []
        self.aulas = {}
        self.progresso = {}
        
        self.setup_window()
        self.setup_ui()
        self.carregar_dados()
        
    def setup_window(self):
        """Configura a janela"""
        self.title(f"Disciplina: {self.disciplina.get('nome', 'Sem nome')}")
        self.geometry("1200x800")
        self.transient(self.master)
        
        # Centraliza a janela
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.winfo_screenheight() // 2) - (800 // 2)
        self.geometry(f"1200x800+{x}+{y}")
        
    def setup_ui(self):
        """Configura a interface da janela"""
        
        # Header com informações da disciplina
        self.create_header()
        
        # Container principal
        main_container = ctk.CTkFrame(self, corner_radius=10)
        main_container.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        
        # Layout horizontal: sidebar (módulos) + conteúdo (aulas)
        self.create_layout(main_container)
        
    def create_header(self):
        """Cria o cabeçalho com informações da disciplina"""
        
        header = ctk.CTkFrame(self, height=80, corner_radius=10)
        header.pack(fill="x", padx=20, pady=20)
        header.pack_propagate(False)
        
        # Container para organizar header
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(expand=True, fill="both", padx=20, pady=15)
        
        # Título da disciplina
        titulo = ctk.CTkLabel(
            header_content,
            text=f"📚 {self.disciplina.get('nome', 'Disciplina')}",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        titulo.pack(anchor="w")
        
        # Informações extras
        info_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        info_frame.pack(fill="x", pady=(5, 0))
        
        curso_info = f"🎓 Curso: {self.disciplina.get('curso_nome', 'Não informado')}"
        curso_label = ctk.CTkLabel(
            info_frame,
            text=curso_info,
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        curso_label.pack(side="left")
        
        # Progresso da disciplina
        progresso = self.disciplina.get('progresso', {})
        if progresso:
            progresso_text = f"📊 Progresso: {progresso.get('aulas_concluidas', 0)}/{progresso.get('total_aulas', 0)} ({progresso.get('percentual', 0)}%)"
            progresso_label = ctk.CTkLabel(
                info_frame,
                text=progresso_text,
                font=ctk.CTkFont(size=12),
                text_color="gray"
            )
            progresso_label.pack(side="right")
        
    def create_layout(self, parent):
        """Cria o layout principal com sidebar e conteúdo"""
        
        # Sidebar para módulos (esquerda)
        self.sidebar = ctk.CTkFrame(parent, width=320, corner_radius=8)
        self.sidebar.pack(side="left", fill="y", padx=(10, 5), pady=10)
        self.sidebar.pack_propagate(False)
        
        # Título da sidebar
        sidebar_title = ctk.CTkLabel(
            self.sidebar,
            text="📖 Módulos",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        sidebar_title.pack(pady=(15, 10))
        
        # Frame scrollável para módulos
        self.modulos_frame = ctk.CTkScrollableFrame(self.sidebar)
        self.modulos_frame.pack(fill="both", expand=True, padx=10, pady=(0, 15))
        
        # Área de conteúdo para aulas (direita)
        self.content_area = ctk.CTkFrame(parent, corner_radius=8)
        self.content_area.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)
        
        # Placeholder inicial
        self.placeholder_label = ctk.CTkLabel(
            self.content_area,
            text="📋 Selecione um módulo para visualizar as aulas",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.placeholder_label.pack(expand=True)
        
    def carregar_dados(self):
        """Carrega módulos, aulas e progresso da disciplina"""
        try:
            # Carrega módulos
            modulos_response = listar_modulos_disciplina(self.disciplina['id'])
            if modulos_response.get("status") == "ok":
                self.modulos = modulos_response.get("data", [])
            
            # Carrega aulas para cada módulo
            for modulo in self.modulos:
                aulas_response = listar_aulas_modulo(modulo['id'])
                if aulas_response.get("status") == "ok":
                    self.aulas[modulo['id']] = aulas_response.get("data", [])
                    
            # Carrega progresso do aluno
            progresso_response = obter_progresso_aluno(self.aluno_id, self.disciplina['id'])
            if progresso_response.get("status") == "ok":
                progresso_list = progresso_response.get("data", [])
                self.progresso = {p['aula_id']: p for p in progresso_list}
                
            # Atualiza interface
            self.atualizar_modulos()
            
        except Exception as e:
            self.show_error(f"Erro ao carregar dados: {str(e)}")
            
    def atualizar_modulos(self):
        """Atualiza a lista de módulos na sidebar"""
        
        # Remove widgets anteriores
        for widget in self.modulos_frame.winfo_children():
            widget.destroy()
            
        if not self.modulos:
            empty_label = ctk.CTkLabel(
                self.modulos_frame,
                text="📭 Nenhum módulo encontrado",
                text_color="gray"
            )
            empty_label.pack(pady=20)
            return
            
        # Cria cards para cada módulo
        for i, modulo in enumerate(self.modulos):
            modulo_card = self.create_modulo_card(self.modulos_frame, modulo, i)
            modulo_card.pack(fill="x", pady=5, padx=5)
    
    def create_modulo_card(self, parent, modulo, index):
        """Cria um card para um módulo"""
        
        # Calcula estatísticas do módulo
        aulas_modulo = self.aulas.get(modulo['id'], [])
        total_aulas = len(aulas_modulo)
        aulas_concluidas = sum(1 for aula in aulas_modulo 
                              if self.progresso.get(aula['id'], {}).get('concluida', False))
        
        # Card do módulo
        card = ctk.CTkFrame(parent, corner_radius=6)
        
        # Número e nome do módulo
        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        numero_label = ctk.CTkLabel(
            header_frame,
            text=f"Módulo {index + 1}",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="gray"
        )
        numero_label.pack(anchor="w")
        
        nome_label = ctk.CTkLabel(
            header_frame,
            text=modulo.get('nome', 'Sem nome'),
            font=ctk.CTkFont(size=13, weight="bold"),
            wraplength=250
        )
        nome_label.pack(anchor="w", pady=(2, 0))
        
        # Descrição (se existir)
        descricao = modulo.get('descricao', '').strip()
        if descricao:
            desc_label = ctk.CTkLabel(
                card,
                text=descricao,
                font=ctk.CTkFont(size=10),
                text_color="gray",
                wraplength=250
            )
            desc_label.pack(anchor="w", padx=10, pady=(0, 5))
        
        # Estatísticas
        stats_text = f"📊 {aulas_concluidas}/{total_aulas} aulas"
        stats_label = ctk.CTkLabel(
            card,
            text=stats_text,
            font=ctk.CTkFont(size=10),
            text_color="blue"
        )
        stats_label.pack(anchor="w", padx=10)
        
        # Botão para expandir
        btn = ctk.CTkButton(
            card,
            text="Ver Aulas",
            command=lambda: self.mostrar_aulas_modulo(modulo),
            height=30,
            corner_radius=6
        )
        btn.pack(fill="x", padx=10, pady=(5, 10))
        
        return card
        
    def mostrar_aulas_modulo(self, modulo):
        """Mostra as aulas de um módulo na área de conteúdo"""
        
        # Remove placeholder/conteúdo anterior
        for widget in self.content_area.winfo_children():
            widget.destroy()
            
        # Header da área de conteúdo
        header = ctk.CTkFrame(self.content_area, height=60, corner_radius=8)
        header.pack(fill="x", padx=15, pady=(15, 10))
        header.pack_propagate(False)
        
        titulo = ctk.CTkLabel(
            header,
            text=f"🎯 {modulo.get('nome', 'Módulo')}",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        titulo.pack(pady=15)
        
        # Frame scrollável para aulas
        aulas_frame = ctk.CTkScrollableFrame(self.content_area)
        aulas_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Lista aulas
        aulas_modulo = self.aulas.get(modulo['id'], [])
        if not aulas_modulo:
            empty_label = ctk.CTkLabel(
                aulas_frame,
                text="📭 Nenhuma aula encontrada neste módulo",
                font=ctk.CTkFont(size=14),
                text_color="gray"
            )
            empty_label.pack(pady=50)
            return
            
        # Ordena aulas por sequência
        aulas_ordenadas = sorted(aulas_modulo, key=lambda x: x.get('sequencia', 0))
        
        for i, aula in enumerate(aulas_ordenadas):
            aula_card = self.create_aula_card(aulas_frame, aula, i + 1)
            aula_card.pack(fill="x", pady=8, padx=10)
            
    def create_aula_card(self, parent, aula, numero):
        """Cria um card para uma aula"""
        
        # Verifica se a aula foi concluída
        concluida = self.progresso.get(aula['id'], {}).get('concluida', False)
        
        # Card da aula
        card = ctk.CTkFrame(parent, corner_radius=8)
        
        # Header da aula com botão expansível
        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        # Lado esquerdo - info da aula
        left_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="x", expand=True)
        
        # Número e título
        numero_titulo = f"Aula {numero}: {aula.get('titulo', 'Sem título')}"
        titulo_label = ctk.CTkLabel(
            left_frame,
            text=numero_titulo,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        titulo_label.pack(anchor="w")
        
        # Status
        status_text = "✅ Concluída" if concluida else "⏳ Pendente"
        status_color = "green" if concluida else "orange"
        status_label = ctk.CTkLabel(
            left_frame,
            text=status_text,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=status_color
        )
        status_label.pack(anchor="w", pady=(5, 0))
        
        # Lado direito - botões de ação (todos alinhados horizontalmente)
        action_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        action_frame.pack(side="right")
        
        # Variável para controlar expansão
        card.expanded = False
        
        def toggle_content():
            if hasattr(card, 'content_frame'):
                if card.expanded:
                    card.content_frame.pack_forget()
                    expand_btn.configure(text="📖 Expandir Conteúdo")
                    card.expanded = False
                else:
                    card.content_frame.pack(fill="x", padx=15, pady=(5, 15), after=header_frame)
                    expand_btn.configure(text="📚 Colapsar")
                    card.expanded = True
        
        # Botão para expandir conteúdo
        expand_btn = ctk.CTkButton(
            action_frame,
            text="📖 Expandir Conteúdo",
            command=toggle_content,
            height=35,
            width=160,
            font=ctk.CTkFont(size=11),
            fg_color=("blue", "blue"),
            hover_color=("darkblue", "darkblue")
        )
        expand_btn.pack(side="left", padx=(0, 5))
        
        # Botão de vídeo (se existir)
        video_url = aula.get('video_url', '').strip()
        if video_url:
            video_btn = ctk.CTkButton(
                action_frame,
                text="🎥 Assistir Vídeo",
                command=lambda: self.abrir_video(video_url),
                height=35,
                width=120,
                fg_color="red",
                hover_color="darkred"
            )
            video_btn.pack(side="left", padx=(0, 5))
        
        # Botão marcar como concluída
        if not concluida:
            concluir_btn = ctk.CTkButton(
                action_frame,
                text="✓ Concluir",
                command=lambda: self.marcar_concluida(aula['id']),
                height=35,
                width=100,
                fg_color="green",
                hover_color="darkgreen"
            )
            concluir_btn.pack(side="left")
            
        # Frame expansível para conteúdo (inicialmente oculto)
        resumo = aula.get('resumo', '').strip()
        if resumo:
            content_frame = ctk.CTkFrame(card, fg_color=("gray90", "gray20"), corner_radius=8)
            
            # Scrollable text area para conteúdo longo
            content_scroll = ctk.CTkScrollableFrame(content_frame, height=200)
            content_scroll.pack(fill="both", expand=True, padx=10, pady=10)
            
            content_label = ctk.CTkLabel(
                content_scroll,
                text=resumo,
                font=ctk.CTkFont(size=12),
                wraplength=650,
                justify="left",
                anchor="nw"
            )
            content_label.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Salva referência do frame de conteúdo
            card.content_frame = content_frame
        
        return card
        
    def abrir_video(self, video_url):
        """Abre o vídeo da aula no navegador"""
        try:
            import webbrowser
            webbrowser.open(video_url)
            self.show_success("Vídeo aberto no navegador!")
        except Exception as e:
            self.show_error(f"Erro ao abrir vídeo: {str(e)}")
    
    def marcar_concluida(self, aula_id):
        """Marca uma aula como concluída"""        
        try:
            response = marcar_aula_concluida(self.aluno_id, aula_id)
            if response.get("status") == "ok":
                # Atualiza progresso local
                self.progresso[aula_id] = {"concluida": True}
                
                # Recarrega a view do módulo atual
                self.show_success("Aula marcada como concluída!")
                
                # Recarregar dados para atualizar interface
                self.carregar_dados()
            else:
                self.show_error(f"Erro: {response.get('message', 'Erro desconhecido')}")
                
        except Exception as e:
            self.show_error(f"Erro ao marcar aula: {str(e)}")
            
    def show_success(self, message):
        """Mostra mensagem de sucesso""" 
        # Cria popup temporário de sucesso
        popup = ctk.CTkToplevel(self)
        popup.geometry("300x100")
        popup.title("Sucesso")
        popup.transient(self)
        
        # Centraliza popup
        popup.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - 150
        y = self.winfo_y() + (self.winfo_height() // 2) - 50
        popup.geometry(f"300x100+{x}+{y}")
        
        label = ctk.CTkLabel(popup, text=f"✅ {message}", 
                            font=ctk.CTkFont(size=12, weight="bold"),
                            text_color="green")
        label.pack(expand=True)
        
        # Auto fecha em 2 segundos
        popup.after(2000, popup.destroy)
        
    def show_error(self, message):
        """Mostra mensagem de erro"""
        # Cria popup temporário de erro
        popup = ctk.CTkToplevel(self)
        popup.geometry("300x100")
        popup.title("Erro")
        popup.transient(self)
        
        # Centraliza popup
        popup.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - 150
        y = self.winfo_y() + (self.winfo_height() // 2) - 50
        popup.geometry(f"300x100+{x}+{y}")
        
        label = ctk.CTkLabel(popup, text=f"⚠️ {message}", 
                            font=ctk.CTkFont(size=12, weight="bold"),
                            text_color="red")
        label.pack(expand=True)
        
        # Auto fecha em 3 segundos
        popup.after(3000, popup.destroy)