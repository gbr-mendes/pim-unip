import customtkinter as ctk
from view.professor.components.discipline_components import CourseSection, EmptyState
from view.professor.components.search_filter import SearchAndFilterWidget
from view.professor.components.stats_widget import StatsWidget
from controller.discipline_controller import listar_disciplinas
from controller.course_controller import listar_cursos
from session import get_usuario

def criar_dashboard_professor(root):
    """Cria o dashboard do professor com suas disciplinas organizadas por curso"""
    global _stats_widget, _main_window
    
    # Armazena referência da janela principal
    _main_window = root
    
    # Limpa tela
    for widget in root.winfo_children():
        widget.destroy()

    # Container principal
    container = ctk.CTkFrame(root, corner_radius=15)
    container.pack(pady=20, padx=40, fill="both", expand=True)

    # Obtém dados do professor logado
    usuario_logado = get_usuario()
    if not usuario_logado:
        ctk.CTkLabel(container, text="Erro: Usuário não logado", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        return

    # Título
    titulo = ctk.CTkLabel(container, 
                         text=f"Dashboard do Professor - {usuario_logado.get('nome', '')} {usuario_logado.get('sobrenome', '')}", 
                         font=ctk.CTkFont(size=22, weight="bold"))
    titulo.pack(pady=20)

    # Widget de estatísticas
    _stats_widget = StatsWidget(container, corner_radius=10)
    _stats_widget.pack(fill="x", pady=10, padx=10)

    # Widget de busca e filtro
    search_widget = SearchAndFilterWidget(
        container,
        on_search_change=lambda text: filtrar_disciplinas(content_frame, text, search_widget.get_selected_course()),
        on_filter_change=lambda course: filtrar_disciplinas(content_frame, search_widget.get_search_text(), course)
    )
    search_widget.pack(fill="x", pady=10, padx=10)

    # Frame para conteúdo principal
    content_frame = ctk.CTkScrollableFrame(container)
    content_frame.pack(fill="both", expand=True, pady=10, padx=10)

    # Carrega e organiza as disciplinas do professor
    carregar_disciplinas_professor(content_frame, usuario_logado.get('id'), search_widget, _stats_widget)

# Variáveis globais para filtros
_all_disciplinas = []
_all_cursos = []
_current_professor_id = None
_stats_widget = None
_main_window = None

def filtrar_disciplinas(content_frame, search_text="", selected_course="Todos os cursos"):
    """Filtra as disciplinas baseado na busca e filtro de curso"""
    if not _all_disciplinas or not _all_cursos:
        return
        
    # Limpa o frame de conteúdo
    for widget in content_frame.winfo_children():
        widget.destroy()
    
    # Filtra disciplinas do professor
    disciplinas_professor = [d for d in _all_disciplinas if d.get('professor_id') == _current_professor_id]
    
    # Aplica filtro de busca
    if search_text:
        disciplinas_professor = [
            d for d in disciplinas_professor 
            if search_text.lower() in d.get('nome', '').lower()
        ]
    
    # Aplica filtro de curso
    if selected_course != "Todos os cursos":
        curso_filtrado = next((c for c in _all_cursos if c['nome'] == selected_course), None)
        if curso_filtrado:
            disciplinas_professor = [
                d for d in disciplinas_professor 
                if d.get('curso_id') == curso_filtrado['id']
            ]
    
    # Atualiza estatísticas com dados filtrados
    if _stats_widget:
        _stats_widget.update_stats(disciplinas_professor, _all_cursos)
    
    if not disciplinas_professor:
        empty_frame = EmptyState(
            content_frame,
            message="Nenhuma disciplina encontrada com os filtros aplicados.",
            icon="🔍"
        )
        empty_frame.pack(fill="both", expand=True, pady=50)
        return
    
    # Organiza disciplinas por curso
    cursos_dict = {curso['id']: curso for curso in _all_cursos}
    disciplinas_por_curso = {}
    
    for disciplina in disciplinas_professor:
        curso_id = disciplina.get('curso_id')
        if curso_id not in disciplinas_por_curso:
            disciplinas_por_curso[curso_id] = []
        disciplinas_por_curso[curso_id].append(disciplina)

    # Cria seções para cada curso
    for curso_id, disciplinas_curso in disciplinas_por_curso.items():
        curso = cursos_dict.get(curso_id, {'nome': 'Curso não encontrado', 'id': curso_id})
        
        course_section = CourseSection(
            content_frame,
            curso,
            disciplinas_curso,
            on_disciplina_click=on_disciplina_click,
            corner_radius=10
        )
        course_section.pack(fill="x", pady=10, padx=5)

def carregar_disciplinas_professor(content_frame, professor_id, search_widget=None, stats_widget=None):
    """Carrega e exibe as disciplinas do professor organizadas por curso"""
    global _all_disciplinas, _all_cursos, _current_professor_id
    
    try:
        # Obtém dados
        disciplinas_response = listar_disciplinas()
        cursos_response = listar_cursos()
        
        if disciplinas_response.get("status") != "ok" or cursos_response.get("status") != "ok":
            error_frame = EmptyState(
                content_frame, 
                message="Erro ao carregar dados do servidor",
                icon="⚠️"
            )
            error_frame.pack(fill="both", expand=True, pady=20)
            return

        _all_disciplinas = disciplinas_response.get("data", [])
        _all_cursos = cursos_response.get("data", [])
        _current_professor_id = professor_id
        
        # Filtra disciplinas do professor
        disciplinas_professor = [d for d in _all_disciplinas if d.get('professor_id') == professor_id]
        
        # Atualiza estatísticas
        if stats_widget:
            stats_widget.update_stats(disciplinas_professor, _all_cursos)
        
        # Atualiza opções do filtro de curso
        if search_widget:
            # Filtra cursos que têm disciplinas do professor
            cursos_professor = []
            for disciplina in disciplinas_professor:
                curso = next((c for c in _all_cursos if c['id'] == disciplina.get('curso_id')), None)
                if curso and curso not in cursos_professor:
                    cursos_professor.append(curso)
            
            search_widget.update_course_options(cursos_professor)
        
        if not disciplinas_professor:
            empty_frame = EmptyState(
                content_frame,
                message="Nenhuma disciplina atribuída a você ainda.",
                icon="📚"
            )
            empty_frame.pack(fill="both", expand=True, pady=50)
            return

        # Organiza disciplinas por curso
        cursos_dict = {curso['id']: curso for curso in _all_cursos}
        disciplinas_por_curso = {}
        
        for disciplina in disciplinas_professor:
            curso_id = disciplina.get('curso_id')
            if curso_id not in disciplinas_por_curso:
                disciplinas_por_curso[curso_id] = []
            disciplinas_por_curso[curso_id].append(disciplina)

        # Cria seções para cada curso
        for curso_id, disciplinas_curso in disciplinas_por_curso.items():
            curso = cursos_dict.get(curso_id, {'nome': 'Curso não encontrado', 'id': curso_id})
            
            course_section = CourseSection(
                content_frame,
                curso,
                disciplinas_curso,
                on_disciplina_click=on_disciplina_click,
                corner_radius=10
            )
            course_section.pack(fill="x", pady=10, padx=5)

    except Exception as e:
        error_frame = EmptyState(
            content_frame,
            message=f"Erro ao carregar disciplinas: {str(e)}",
            icon="⚠️"
        )
        error_frame.pack(fill="both", expand=True, pady=20)

def on_disciplina_click(disciplina):
    """Callback para quando uma disciplina é clicada"""
    from view.professor.discipline_management import DisciplineManagementView
    
    # Abre janela de gerenciamento da disciplina
    try:
        global _main_window
        
        if _main_window:
            management_window = DisciplineManagementView(_main_window, disciplina)
        else:
            print("Erro: Referência da janela principal não encontrada")
            
    except Exception as e:
        print(f"Erro ao abrir gerenciamento da disciplina: {str(e)}")
        import traceback
        traceback.print_exc()