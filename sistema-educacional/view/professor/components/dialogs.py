import customtkinter as ctk
import webbrowser
import re

class ModuloDialog(ctk.CTkToplevel):
    """Dialog para criar/editar módulo"""
    
    def __init__(self, parent, title, modulo=None):
        super().__init__(parent)
        
        self.result = None
        self.modulo = modulo
        
        self.setup_window(title)
        self.create_ui()
        
        # Se está editando, preenche os campos
        if self.modulo:
            self.nome_entry.insert(0, self.modulo['nome'])
            self.descricao_text.insert("1.0", self.modulo.get('descricao', ''))
        
        # Foca no primeiro campo
        self.nome_entry.focus()
        
        # Espera o resultado
        self.wait_window()
        
    def setup_window(self, title):
        """Configura a janela"""
        self.title(title)
        self.geometry("500x450")  # Aumentei a altura
        self.resizable(False, False)
        
        # Centraliza
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.winfo_screenheight() // 2) - (450 // 2)
        self.geometry(f"500x450+{x}+{y}")
        
        # Modal
        self.transient(self.master)
        self.grab_set()
        
    def create_ui(self):
        """Cria a interface"""
        # Container principal
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ctk.CTkLabel(
            main_frame,
            text="📂 Módulo",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(10, 20))
        
        # Campo nome
        ctk.CTkLabel(
            main_frame,
            text="Nome do Módulo:",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w", pady=(10, 5))
        
        self.nome_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="Ex: Introdução ao Python",
            font=ctk.CTkFont(size=12),
            height=35
        )
        self.nome_entry.pack(fill="x", pady=(0, 15))
        
        # Campo descrição
        ctk.CTkLabel(
            main_frame,
            text="Descrição (opcional):",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w", pady=(0, 5))
        
        self.descricao_text = ctk.CTkTextbox(
            main_frame,
            height=120,  # Reduzi a altura para dar espaço aos botões
            font=ctk.CTkFont(size=12)
        )
        self.descricao_text.pack(fill="both", expand=True, pady=(0, 15))
        
        # Botões - frame fixo no final
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(10, 15), side="bottom")
        
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="✅ Salvar",
            command=self.save,
            height=35,
            width=100
        )
        save_btn.pack(side="right", padx=(5, 10))
        
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="❌ Cancelar",
            command=self.cancel,
            fg_color="gray",
            hover_color="darkgray",
            height=35,
            width=100
        )
        cancel_btn.pack(side="right", padx=5)
        
        # Bind Enter para salvar
        self.bind('<Return>', lambda e: self.save())
        
    def save(self):
        """Salva o módulo"""
        nome = self.nome_entry.get().strip()
        if not nome:
            self.show_error("Nome do módulo é obrigatório!")
            return
            
        descricao = self.descricao_text.get("1.0", "end-1c").strip()
        
        self.result = (nome, descricao)
        self.destroy()
        
    def cancel(self):
        """Cancela o dialog"""
        self.destroy()
        
    def show_error(self, message):
        """Mostra erro"""
        error_dialog = ctk.CTkToplevel(self)
        error_dialog.title("Erro")
        error_dialog.geometry("300x150")
        error_dialog.transient(self)
        error_dialog.grab_set()
        
        # Centraliza
        error_dialog.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (300 // 2)
        y = (self.winfo_screenheight() // 2) - (150 // 2)
        error_dialog.geometry(f"300x150+{x}+{y}")
        
        ctk.CTkLabel(
            error_dialog,
            text="❌ " + message,
            font=ctk.CTkFont(size=14)
        ).pack(pady=30)
        
        ctk.CTkButton(
            error_dialog,
            text="OK",
            command=error_dialog.destroy
        ).pack(pady=10)

class AulaDialog(ctk.CTkToplevel):
    """Dialog para criar/editar aula"""
    
    def __init__(self, parent, title, aula=None):
        super().__init__(parent)
        
        self.result = None
        self.aula = aula
        
        self.setup_window(title)
        self.create_ui()
        
        # Se está editando, preenche os campos
        if self.aula:
            self.titulo_entry.insert(0, self.aula['titulo'])
            self.resumo_text.insert("1.0", self.aula.get('resumo', ''))
            self.video_entry.insert(0, self.aula.get('video_url', ''))
        
        # Foca no primeiro campo
        self.titulo_entry.focus()
        
        # Espera o resultado
        self.wait_window()
        
    def setup_window(self, title):
        """Configura a janela"""
        self.title(title)
        self.geometry("600x550")  # Aumentei a altura
        self.resizable(False, False)
        
        # Centraliza
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.winfo_screenheight() // 2) - (550 // 2)
        self.geometry(f"600x550+{x}+{y}")
        
        # Modal
        self.transient(self.master)
        self.grab_set()
        
    def create_ui(self):
        """Cria a interface"""
        # Container principal
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ctk.CTkLabel(
            main_frame,
            text="🎥 Aula",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(10, 20))
        
        # Campo título
        ctk.CTkLabel(
            main_frame,
            text="Título da Aula:",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w", pady=(10, 5))
        
        self.titulo_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="Ex: Variáveis e Tipos de Dados",
            font=ctk.CTkFont(size=12),
            height=35
        )
        self.titulo_entry.pack(fill="x", pady=(0, 15))
        
        # Campo resumo
        ctk.CTkLabel(
            main_frame,
            text="Resumo do Conteúdo:",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w", pady=(0, 5))
        
        self.resumo_text = ctk.CTkTextbox(
            main_frame,
            height=120,  # Reduzi a altura para dar espaço aos botões
            font=ctk.CTkFont(size=12)
        )
        self.resumo_text.pack(fill="both", expand=True, pady=(0, 15))
        
        # Campo vídeo
        ctk.CTkLabel(
            main_frame,
            text="URL do Vídeo (obrigatório):*",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="red"
        ).pack(anchor="w", pady=(0, 5))
        
        video_frame = ctk.CTkFrame(main_frame)
        video_frame.pack(fill="x", pady=(0, 20))
        
        self.video_entry = ctk.CTkEntry(
            video_frame,
            placeholder_text="https://www.youtube.com/watch?v=...",
            font=ctk.CTkFont(size=12),
            height=35
        )
        self.video_entry.pack(side="left", fill="x", expand=True, padx=(5, 10), pady=5)
        
        test_video_btn = ctk.CTkButton(
            video_frame,
            text="🔗 Testar",
            width=80,
            command=self.test_video_url,
            fg_color="blue",
            hover_color="darkblue"
        )
        test_video_btn.pack(side="right", padx=5, pady=5)
        
        # Botões - frame fixo no final
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(10, 15), side="bottom")
        
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="✅ Salvar",
            command=self.save,
            height=35,
            width=100
        )
        save_btn.pack(side="right", padx=(5, 10))
        
        preview_btn = ctk.CTkButton(
            buttons_frame,
            text="👁️ Preview",
            command=self.preview,
            fg_color="orange",
            hover_color="darkorange",
            height=35,
            width=100
        )
        preview_btn.pack(side="right", padx=5)
        
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="❌ Cancelar",
            command=self.cancel,
            fg_color="gray",
            hover_color="darkgray",
            height=35,
            width=100
        )
        cancel_btn.pack(side="right", padx=5)
        
    def test_video_url(self):
        """Testa a URL do vídeo"""
        url = self.video_entry.get().strip()
        if not url:
            self.show_error("Digite uma URL primeiro!")
            return
            
        if not self.is_valid_video_url(url):
            self.show_error("URL inválida! Use links do YouTube, Vimeo, etc.")
            return
            
        try:
            webbrowser.open(url)
        except Exception as e:
            self.show_error(f"Erro ao abrir URL: {str(e)}")
            
    def is_valid_video_url(self, url):
        """Valida se a URL é de um vídeo"""
        video_patterns = [
            r'youtube\.com/watch\?v=',
            r'youtu\.be/',
            r'vimeo\.com/',
            r'dailymotion\.com/',
        ]
        
        return any(re.search(pattern, url, re.IGNORECASE) for pattern in video_patterns)
        
    def preview(self):
        """Mostra preview da aula"""
        titulo = self.titulo_entry.get().strip()
        resumo = self.resumo_text.get("1.0", "end-1c").strip()
        video_url = self.video_entry.get().strip()
        
        if not titulo:
            self.show_error("Título é obrigatório para o preview!")
            return
            
        # Cria aula temporária para preview
        aula_temp = {
            'titulo': titulo,
            'resumo': resumo,
            'video_url': video_url
        }
        
        preview_dialog = PreviewDialog(self, aula_temp)
        
    def save(self):
        """Salva a aula"""
        titulo = self.titulo_entry.get().strip()
        if not titulo:
            self.show_error("Título da aula é obrigatório!")
            return
            
        resumo = self.resumo_text.get("1.0", "end-1c").strip()
        video_url = self.video_entry.get().strip()
        
        # Vídeo agora é obrigatório
        if not video_url:
            self.show_error("URL do vídeo é obrigatória!")
            return
        
        # Valida URL
        if not self.is_valid_video_url(video_url):
            self.show_error("URL do vídeo inválida! Use links do YouTube, Vimeo, etc.")
            return
        
        self.result = (titulo, resumo, video_url)
        self.destroy()
        
    def cancel(self):
        """Cancela o dialog"""
        self.destroy()
        
    def show_error(self, message):
        """Mostra erro"""
        error_dialog = ctk.CTkToplevel(self)
        error_dialog.title("Erro")
        error_dialog.geometry("350x150")
        error_dialog.transient(self)
        error_dialog.grab_set()
        
        # Centraliza
        error_dialog.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (350 // 2)
        y = (self.winfo_screenheight() // 2) - (150 // 2)
        error_dialog.geometry(f"350x150+{x}+{y}")
        
        ctk.CTkLabel(
            error_dialog,
            text="❌ " + message,
            font=ctk.CTkFont(size=14)
        ).pack(pady=30)
        
        ctk.CTkButton(
            error_dialog,
            text="OK",
            command=error_dialog.destroy
        ).pack(pady=10)

class PreviewDialog(ctk.CTkToplevel):
    """Dialog para preview de aula"""
    
    def __init__(self, parent, aula):
        super().__init__(parent)
        
        self.aula = aula
        
        self.setup_window()
        self.create_ui()
        
    def setup_window(self):
        """Configura a janela"""
        self.title(f"Preview - {self.aula['titulo']}")
        self.geometry("800x600")
        self.resizable(True, True)
        
        # Centraliza
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.winfo_screenheight() // 2) - (600 // 2)
        self.geometry(f"800x600+{x}+{y}")
        
        # Modal
        self.transient(self.master)
        self.grab_set()
        
    def create_ui(self):
        """Cria a interface"""
        # Container principal
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Título
        title_label = ctk.CTkLabel(
            header_frame,
            text=f"🎥 {self.aula['titulo']}",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Container de conteúdo
        content_frame = ctk.CTkScrollableFrame(main_frame)
        content_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Vídeo (se houver)
        if self.aula.get('video_url'):
            video_frame = ctk.CTkFrame(content_frame)
            video_frame.pack(fill="x", pady=(0, 20), padx=10)
            
            ctk.CTkLabel(
                video_frame,
                text="📹 Vídeo da Aula",
                font=ctk.CTkFont(size=16, weight="bold")
            ).pack(pady=(15, 10))
            
            video_info_frame = ctk.CTkFrame(video_frame)
            video_info_frame.pack(fill="x", pady=10, padx=15)
            
            # URL do vídeo
            url_frame = ctk.CTkFrame(video_info_frame)
            url_frame.pack(fill="x", pady=5)
            
            ctk.CTkLabel(
                url_frame,
                text="URL:",
                font=ctk.CTkFont(size=12, weight="bold")
            ).pack(side="left", padx=(10, 5))
            
            url_label = ctk.CTkLabel(
                url_frame,
                text=self.aula['video_url'],
                font=ctk.CTkFont(size=12),
                text_color="blue"
            )
            url_label.pack(side="left", fill="x", expand=True, padx=5)
            
            # Botão para abrir vídeo
            open_video_btn = ctk.CTkButton(
                video_info_frame,
                text="🔗 Abrir Vídeo",
                command=self.open_video,
                height=35
            )
            open_video_btn.pack(pady=10)
        
        # Resumo
        if self.aula.get('resumo'):
            resumo_frame = ctk.CTkFrame(content_frame)
            resumo_frame.pack(fill="both", expand=True, pady=10, padx=10)
            
            ctk.CTkLabel(
                resumo_frame,
                text="📝 Resumo do Conteúdo",
                font=ctk.CTkFont(size=16, weight="bold")
            ).pack(pady=(15, 10))
            
            resumo_text = ctk.CTkTextbox(
                resumo_frame,
                height=200,
                font=ctk.CTkFont(size=12)
            )
            resumo_text.pack(fill="both", expand=True, pady=10, padx=15)
            resumo_text.insert("1.0", self.aula['resumo'])
            resumo_text.configure(state="disabled")  # Somente leitura
        
        # Botão fechar
        close_btn = ctk.CTkButton(
            main_frame,
            text="Fechar",
            command=self.destroy,
            height=40
        )
        close_btn.pack(pady=10)
        
    def open_video(self):
        """Abre o vídeo no navegador"""
        try:
            webbrowser.open(self.aula['video_url'])
        except Exception as e:
            error_dialog = ctk.CTkToplevel(self)
            error_dialog.title("Erro")
            error_dialog.geometry("300x150")
            error_dialog.transient(self)
            error_dialog.grab_set()
            
            ctk.CTkLabel(
                error_dialog,
                text=f"❌ Erro ao abrir vídeo:\n{str(e)}",
                font=ctk.CTkFont(size=12)
            ).pack(pady=30)
            
            ctk.CTkButton(
                error_dialog,
                text="OK",
                command=error_dialog.destroy
            ).pack(pady=10)