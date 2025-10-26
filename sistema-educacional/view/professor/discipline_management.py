import customtkinter as ctk
from controller.modulo_controller import listar_modulos_disciplina, criar_modulo, excluir_modulo
from controller.aula_controller import listar_aulas_modulo, criar_aula, excluir_aula
from view.professor.components.discipline_components import EmptyState
from view.professor.components.modulo_components import ModuloCard, AulaCard
from view.professor.components.dialogs import ModuloDialog, AulaDialog, PreviewDialog

class DisciplineManagementView(ctk.CTkToplevel):
    """Janela de gerenciamento de uma disciplina específica"""
    
    def __init__(self, parent, disciplina):
        super().__init__(parent)
        
        self.disciplina = disciplina
        self.modulos = []
        self.setup_window()
        self.create_ui()
        self.load_data()
        
    def setup_window(self):
        """Configura a janela"""
        self.title(f"Gerenciar Disciplina - {self.disciplina['nome']}")
        self.geometry("1200x800")
        self.resizable(True, True)
        
        # Torna a janela modal em relação à principal
        self.transient(self.master)
        
        # Centraliza a janela
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.winfo_screenheight() // 2) - (800 // 2)
        self.geometry(f"1200x800+{x}+{y}")
        
        # Configurações para manter a janela em primeiro plano
        self.lift()  # Traz para frente
        self.focus_force()  # Força o foco
        self.attributes("-topmost", True)  # Sempre no topo temporariamente
        
        # Captura todos os eventos (modal)
        self.grab_set()
        
        # Garante que a janela está visível e focada
        self.deiconify()
        self.tkraise()  # Método adicional para trazer para frente
        
        # Remove o topmost após um tempo para permitir interação normal
        # mas mantém a janela modal
        self.after(200, lambda: self.attributes("-topmost", False))
        
        # Força o foco novamente após um pequeno delay
        self.after(100, self.focus_force)
        
        # Bind para manter a janela em foco quando clicada
        self.bind("<Button-1>", self._on_click)
        self.bind("<FocusIn>", self._on_focus)
        
    def _on_click(self, event=None):
        """Traz a janela para frente quando clicada"""
        self.lift()
        self.focus_force()
        
    def _on_focus(self, event=None):
        """Mantém a janela em foco"""
        self.lift()
        
    def create_ui(self):
        """Cria a interface da janela"""
        # Container principal
        main_container = ctk.CTkFrame(self)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ctk.CTkFrame(main_container)
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Título
        title_label = ctk.CTkLabel(
            header_frame,
            text=f"📖 {self.disciplina['nome']}",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Info da disciplina
        info_frame = ctk.CTkFrame(header_frame)
        info_frame.pack(fill="x", pady=10, padx=20)
        
        ctk.CTkLabel(
            info_frame,
            text=f"ID: {self.disciplina['id']} | Curso ID: {self.disciplina.get('curso_id', 'N/A')}",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(pady=10)
        
        # Toolbar
        toolbar_frame = ctk.CTkFrame(main_container)
        toolbar_frame.pack(fill="x", pady=(0, 10))
        
        # Botão adicionar módulo
        add_module_btn = ctk.CTkButton(
            toolbar_frame,
            text="➕ Novo Módulo",
            command=self.show_add_module_dialog,
            height=40
        )
        add_module_btn.pack(side="left", padx=10, pady=10)
        
        # Botão refresh
        refresh_btn = ctk.CTkButton(
            toolbar_frame,
            text="🔄 Atualizar",
            command=self.load_data,
            height=40,
            fg_color="gray",
            hover_color="darkgray"
        )
        refresh_btn.pack(side="right", padx=10, pady=10)
        
        # Container dos módulos
        self.modules_container = ctk.CTkScrollableFrame(main_container)
        self.modules_container.pack(fill="both", expand=True)
        
    def load_data(self):
        """Carrega os dados da disciplina"""
        try:
            # Limpa container
            for widget in self.modules_container.winfo_children():
                widget.destroy()
                
            # Carrega módulos
            response = listar_modulos_disciplina(self.disciplina['id'])
            
            if response.get("status") == "ok":
                self.modulos = response.get("data", [])
                
                if not self.modulos:
                    empty_state = EmptyState(
                        self.modules_container,
                        message="Nenhum módulo criado ainda. Clique em 'Novo Módulo' para começar.",
                        icon="📚"
                    )
                    empty_state.pack(fill="both", expand=True, pady=50)
                else:
                    self.create_module_cards()
            else:
                self.show_error(f"Erro ao carregar módulos: {response.get('message', 'Erro desconhecido')}")
                
        except Exception as e:
            self.show_error(f"Erro inesperado: {str(e)}")
    
    def create_module_cards(self):
        """Cria os cards dos módulos"""
        for modulo in self.modulos:
            module_card = ModuloCard(
                self.modules_container,
                modulo,
                on_add_aula=lambda m=modulo: self.show_add_aula_dialog(m),
                on_edit_modulo=lambda m=modulo: self.show_edit_module_dialog(m),
                on_delete_modulo=lambda m=modulo: self.confirm_delete_module(m),
                on_preview_aula=self.show_preview_aula,
                on_edit_aula=self.show_edit_aula_dialog
            )
            module_card.pack(fill="x", pady=10, padx=5)
            
    def show_add_module_dialog(self):
        """Mostra dialog para adicionar módulo"""
        dialog = ModuloDialog(self, "Novo Módulo")
        if dialog.result:
            nome, descricao = dialog.result
            self.create_module(nome, descricao)
            
    def show_edit_module_dialog(self, modulo):
        """Mostra dialog para editar módulo"""
        dialog = ModuloDialog(self, "Editar Módulo", modulo)
        if dialog.result:
            nome, descricao = dialog.result
            self.update_module(modulo['id'], nome, descricao)
            
    def show_add_aula_dialog(self, modulo):
        """Mostra dialog para adicionar aula"""
        dialog = AulaDialog(self, "Nova Aula")
        if dialog.result:
            titulo, resumo, video_url = dialog.result
            self.create_aula(modulo['id'], titulo, resumo, video_url)
            
    def show_preview_aula(self, aula):
        """Mostra preview da aula"""
        preview = PreviewDialog(self, aula)
        
    def create_module(self, nome, descricao):
        """Cria um novo módulo"""
        try:
            response = criar_modulo(self.disciplina['id'], nome, descricao)
            if response.get("status") == "ok":
                self.show_success("Módulo criado com sucesso!")
                self.load_data()
            else:
                self.show_error(f"Erro ao criar módulo: {response.get('message', 'Erro desconhecido')}")
        except Exception as e:
            self.show_error(f"Erro inesperado: {str(e)}")
            
    def update_module(self, modulo_id, nome, descricao):
        """Atualiza um módulo"""
        try:
            from controller.modulo_controller import atualizar_modulo
            response = atualizar_modulo(modulo_id, nome, descricao)
            if response.get("status") == "ok":
                self.show_success("Módulo atualizado com sucesso!")
                self.load_data()
            else:
                self.show_error(f"Erro ao atualizar módulo: {response.get('message', 'Erro desconhecido')}")
        except Exception as e:
            self.show_error(f"Erro inesperado: {str(e)}")
            
    def create_aula(self, modulo_id, titulo, resumo, video_url):
        """Cria uma nova aula"""
        try:
            response = criar_aula(modulo_id, titulo, resumo, video_url)
            if response.get("status") == "ok":
                self.show_success("Aula criada com sucesso!")
                self.load_data()
            else:
                self.show_error(f"Erro ao criar aula: {response.get('message', 'Erro desconhecido')}")
        except Exception as e:
            self.show_error(f"Erro inesperado: {str(e)}")
            
    def confirm_delete_module(self, modulo):
        """Confirma exclusão do módulo"""
        dialog = ctk.CTkInputDialog(
            text=f"Tem certeza que deseja excluir o módulo '{modulo['nome']}'?\nDigite 'CONFIRMAR' para prosseguir:",
            title="Confirmar Exclusão"
        )
        
        if dialog.get_input() == "CONFIRMAR":
            self.delete_module(modulo['id'])
            
    def delete_module(self, modulo_id):
        """Exclui um módulo"""
        try:
            response = excluir_modulo(modulo_id)
            if response.get("status") == "ok":
                self.show_success("Módulo excluído com sucesso!")
                self.load_data()
            else:
                self.show_error(f"Erro ao excluir módulo: {response.get('message', 'Erro desconhecido')}")
        except Exception as e:
            self.show_error(f"Erro inesperado: {str(e)}")
            
    def show_edit_aula_dialog(self, aula):
        """Mostra dialog para editar aula"""
        dialog = AulaDialog(self, "Editar Aula", aula=aula)
        if dialog.result:
            titulo, resumo, video_url = dialog.result
            self.update_aula(aula['id'], titulo, resumo, video_url)
            
    def update_aula(self, aula_id, titulo, resumo, video_url):
        """Atualiza uma aula"""
        try:
            from controller.aula_controller import atualizar_aula
            response = atualizar_aula(aula_id, titulo, resumo, video_url)
            if response.get("status") == "ok":
                self.show_success("Aula atualizada com sucesso!")
                self.load_data()
            else:
                self.show_error(f"Erro ao atualizar aula: {response.get('message', 'Erro desconhecido')}")
        except Exception as e:
            self.show_error(f"Erro inesperado: {str(e)}")
            
    def show_success(self, message):
        """Mostra mensagem de sucesso"""
        # TODO: Implementar notificação toast
        print(f"SUCCESS: {message}")
        
    def show_error(self, message):
        """Mostra mensagem de erro"""
        # TODO: Implementar notificação toast  
        print(f"ERROR: {message}")
        
        # Por enquanto, mostra em label temporário
        error_label = ctk.CTkLabel(
            self.modules_container,
            text=f"❌ {message}",
            text_color="red",
            font=ctk.CTkFont(size=14)
        )
        error_label.pack(pady=20)
        
        # Remove após 5 segundos
        self.after(5000, error_label.destroy)