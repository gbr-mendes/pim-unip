import customtkinter as ctk
from view.student.components.discipline_card import DisciplineCard
from view.student.components.progress_widget import ProgressWidget
from view.student.components.search_filter import StudentSearchFilter
from view.student.components.module_viewer import ModuleViewer
from controller.aluno_controller import (
    listar_disciplinas_aluno, obter_estatisticas_aluno, buscar_conteudo_aluno
)
from session import get_usuario

def criar_dashboard_aluno(root):
    """Cria o dashboard do aluno com suas disciplinas e progresso"""
    global _progress_widget, _main_window, _all_disciplinas
    
    # Armazena referência da janela principal
    _main_window = root
    
    # Limpa tela
    for widget in root.winfo_children():
        widget.destroy()

    # Container principal
    container = ctk.CTkFrame(root, corner_radius=15)
    container.pack(pady=10, padx=20, fill="both", expand=True)

    # Obtém dados do aluno logado
    usuario_logado = get_usuario()
    if not usuario_logado:
        ctk.CTkLabel(container, text="Erro: Usuário não logado", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        return

    # Header compacto
    header_frame = ctk.CTkFrame(container, height=120, corner_radius=10)
    header_frame.pack(fill="x", pady=(10, 5), padx=10)
    header_frame.pack_propagate(False)
    
    # Frame para título e botão refresh
    title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
    title_frame.pack(fill="x", pady=(10, 0), padx=10)
    
    # Título compacto
    titulo = ctk.CTkLabel(title_frame, 
                         text=f"Portal do Aluno - {usuario_logado.get('nome', '')} {usuario_logado.get('sobrenome', '')}", 
                         font=ctk.CTkFont(size=18, weight="bold"))
    titulo.pack(side="left")

    # Botão de refresh (comando será definido depois)
    refresh_btn = ctk.CTkButton(
        title_frame,
        text="🔄 Atualizar",
        width=100,
        height=30,
        font=ctk.CTkFont(size=12)
    )
    refresh_btn.pack(side="right")

    # Widget de progresso compacto dentro do header
    _progress_widget = ProgressWidget(header_frame, corner_radius=8, height=60)
    _progress_widget.pack(fill="x", pady=(5, 10), padx=20)

    # Widget de busca e filtro compacto
    search_widget = StudentSearchFilter(
        container,
        on_search_change=lambda text: filtrar_disciplinas(content_frame, text, search_widget.get_selected_filter()),
        on_filter_change=lambda filter_type: filtrar_disciplinas(content_frame, search_widget.get_search_text(), filter_type),
        on_buscar_conteudo=lambda termo: buscar_conteudo_global(termo)
    )
    search_widget.pack(fill="x", pady=(5, 10), padx=10)

    # Frame para conteúdo principal - MAIOR ÁREA
    content_frame = ctk.CTkScrollableFrame(container, corner_radius=10)
    content_frame.pack(fill="both", expand=True, pady=(0, 10), padx=10)

    # Função de refresh (agora com todas as variáveis disponíveis)
    def refresh_dashboard():
        """Atualiza os dados do dashboard"""
        print("DEBUG: Atualizando dashboard...")
        # Limpa filtros de busca
        search_widget.clear_search()
        # Força atualização das variáveis globais
        global _all_disciplinas
        _all_disciplinas = []
        # Recarrega dados
        carregar_dados_aluno(content_frame, usuario_logado.get('id'), search_widget, _progress_widget)
        print("DEBUG: Dashboard atualizado!")
    
    # Atualiza o comando do botão
    refresh_btn.configure(command=refresh_dashboard)

    # Carrega disciplinas e estatísticas do aluno
    carregar_dados_aluno(content_frame, usuario_logado.get('id'), search_widget, _progress_widget)

# Variáveis globais
_all_disciplinas = []
_current_aluno_id = None
_progress_widget = None
_main_window = None

def filtrar_disciplinas(content_frame, search_text="", filter_type="Todas"):
    """Filtra as disciplinas baseado na busca e filtro de progresso"""
    if not _all_disciplinas:
        return
        
    # Limpa o frame de conteúdo
    for widget in content_frame.winfo_children():
        widget.destroy()
    
    disciplinas_filtradas = _all_disciplinas.copy()
    
    # Aplica filtro de busca
    if search_text:
        disciplinas_filtradas = [
            d for d in disciplinas_filtradas 
            if search_text.lower() in d.get('nome', '').lower() or
               search_text.lower() in d.get('curso_nome', '').lower()
        ]
    
    # Aplica filtro de progresso
    if filter_type == "Concluídas":
        disciplinas_filtradas = [
            d for d in disciplinas_filtradas 
            if d.get('progresso', {}).get('percentual', 0) >= 100
        ]
    elif filter_type == "Em andamento":
        disciplinas_filtradas = [
            d for d in disciplinas_filtradas 
            if 0 < d.get('progresso', {}).get('percentual', 0) < 100
        ]
    elif filter_type == "Não iniciadas":
        disciplinas_filtradas = [
            d for d in disciplinas_filtradas 
            if d.get('progresso', {}).get('percentual', 0) == 0
        ]
    
    if not disciplinas_filtradas:
        empty_label = ctk.CTkLabel(
            content_frame,
            text="📚 Nenhuma disciplina encontrada com os filtros aplicados.",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        empty_label.pack(pady=50)
        return
    
    # Cria cards das disciplinas
    criar_cards_disciplinas(content_frame, disciplinas_filtradas)

def criar_cards_disciplinas(content_frame, disciplinas):
    """Cria cards visuais para as disciplinas"""
    # Container para organizar em grid
    grid_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    grid_frame.pack(fill="both", expand=True, pady=10)
    
    # Organiza disciplinas em grid de 2 colunas
    for i, disciplina in enumerate(disciplinas):
        row = i // 2
        col = i % 2
        
        card = DisciplineCard(
            grid_frame,
            disciplina,
            on_click=lambda d=disciplina: on_disciplina_click(d),
            corner_radius=10
        )
        card.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
        
    # Configura expansão das colunas
    grid_frame.grid_columnconfigure(0, weight=1)
    grid_frame.grid_columnconfigure(1, weight=1)

def carregar_dados_aluno(content_frame, aluno_id, search_widget=None, progress_widget=None):
    """Carrega e exibe as disciplinas e estatísticas do aluno"""
    global _all_disciplinas, _current_aluno_id
    
    try:
        print(f"DEBUG: Carregando dados para aluno ID: {aluno_id}")
        
        # LIMPA O CONTENT FRAME ANTES DE RECARREGAR
        for widget in content_frame.winfo_children():
            widget.destroy()
        
        # Obtém dados
        disciplinas_response = listar_disciplinas_aluno(aluno_id)
        print(f"DEBUG: Resposta disciplinas: {disciplinas_response}")
        
        estatisticas_response = obter_estatisticas_aluno(aluno_id)
        print(f"DEBUG: Resposta estatísticas: {estatisticas_response}")
        
        if disciplinas_response.get("status") != "ok":
            print(f"DEBUG: Erro no status das disciplinas: {disciplinas_response}")
            error_label = ctk.CTkLabel(
                content_frame, 
                text=f"⚠️ Erro ao carregar disciplinas: {disciplinas_response.get('message', 'Erro desconhecido')}",
                font=ctk.CTkFont(size=16),
                text_color="red"
            )
            error_label.pack(pady=20)
            return

        _all_disciplinas = disciplinas_response.get("data", [])
        _current_aluno_id = aluno_id
        
        print(f"DEBUG: Disciplinas carregadas: {len(_all_disciplinas)} disciplinas")
        print(f"DEBUG: Dados das disciplinas: {_all_disciplinas}")
        
        # Atualiza estatísticas
        if progress_widget and estatisticas_response.get("status") == "ok":
            print(f"DEBUG: Atualizando widget de progresso com dados: {estatisticas_response.get('data', {})}")
            progress_widget.update_stats(estatisticas_response.get("data", {}))
        else:
            print(f"DEBUG: Widget de progresso não será atualizado - Widget: {progress_widget}, Status: {estatisticas_response.get('status')}")
        
        if not _all_disciplinas:
            print("DEBUG: Nenhuma disciplina encontrada")
            empty_label = ctk.CTkLabel(
                content_frame,
                text="📚 Você ainda não está matriculado em nenhuma disciplina.",
                font=ctk.CTkFont(size=16),
                text_color="gray"
            )
            empty_label.pack(pady=50)
            return

        # Cria cards das disciplinas
        print(f"DEBUG: Criando cards para {len(_all_disciplinas)} disciplinas")
        criar_cards_disciplinas(content_frame, _all_disciplinas)

    except Exception as e:
        print(f"DEBUG: Exceção no carregamento: {str(e)}")
        import traceback
        traceback.print_exc()
        error_label = ctk.CTkLabel(
            content_frame,
            text=f"⚠️ Erro ao carregar dados: {str(e)}",
            font=ctk.CTkFont(size=16),
            text_color="red"
        )
        error_label.pack(pady=20)

def on_disciplina_click(disciplina):
    """Callback para quando uma disciplina é clicada"""
    try:
        global _main_window
        
        if _main_window:
            # Abre janela de visualização da disciplina
            viewer_window = ModuleViewer(_main_window, disciplina, _current_aluno_id)
        else:
            print("Erro: Referência da janela principal não encontrada")
            
    except Exception as e:
        print(f"Erro ao abrir visualização da disciplina: {str(e)}")
        import traceback
        traceback.print_exc()

def buscar_conteudo_global(termo):
    """Realiza busca global no conteúdo das disciplinas do aluno"""
    if not _current_aluno_id or not termo.strip():
        return
        
    try:
        resultado = buscar_conteudo_aluno(_current_aluno_id, termo)
        
        if resultado.get("status") == "ok":
            # Cria janela de resultados
            mostrar_resultados_busca(resultado.get("data", []), termo)
        else:
            print(f"Erro na busca: {resultado.get('message', 'Erro desconhecido')}")
            
    except Exception as e:
        print(f"Erro ao buscar conteúdo: {str(e)}")

def mostrar_resultados_busca(resultados, termo):
    """Mostra os resultados da busca em uma janela separada"""
    global _main_window
    
    if not _main_window:
        return
    
    # Cria janela de resultados
    resultado_window = ctk.CTkToplevel(_main_window)
    resultado_window.title(f"Resultados da busca: '{termo}'")
    resultado_window.geometry("800x600")
    resultado_window.transient(_main_window)
    
    # Título
    titulo = ctk.CTkLabel(
        resultado_window,
        text=f"Resultados para: '{termo}' ({len(resultados)} encontrado(s))",
        font=ctk.CTkFont(size=18, weight="bold")
    )
    titulo.pack(pady=20)
    
    if not resultados:
        empty_label = ctk.CTkLabel(
            resultado_window,
            text="🔍 Nenhum resultado encontrado",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        empty_label.pack(pady=50)
        return
    
    # Frame scrollable para resultados
    scroll_frame = ctk.CTkScrollableFrame(resultado_window)
    scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Lista resultados
    for resultado in resultados:
        resultado_frame = ctk.CTkFrame(scroll_frame)
        resultado_frame.pack(fill="x", pady=5, padx=10)
        
        # Título do resultado
        titulo_resultado = f"{resultado['tipo'].title()}: {resultado['titulo']}"
        ctk.CTkLabel(
            resultado_frame,
            text=titulo_resultado,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        # Informações do contexto
        contexto = f"Disciplina: {resultado['disciplina']}"
        if resultado['tipo'] == 'aula':
            contexto += f" | Módulo: {resultado['modulo']}"
            
        ctk.CTkLabel(
            resultado_frame,
            text=contexto,
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(anchor="w", padx=15)
        
        # Conteúdo (limitado)
        conteudo = resultado.get('conteudo', '')
        if len(conteudo) > 150:
            conteudo = conteudo[:150] + "..."
            
        if conteudo:
            ctk.CTkLabel(
                resultado_frame,
                text=conteudo,
                font=ctk.CTkFont(size=11),
                wraplength=750
            ).pack(anchor="w", padx=15, pady=(0, 10))