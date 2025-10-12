import customtkinter as ctk
from .tabs.admin_tab import create_admin_tab
from .tabs.student_tab import create_student_tab
from .tabs.professor_tab import create_professor_tab
from .tabs.course_tab import create_course_tab
from .tabs.discipline_tab import create_discipline_tab
from .tabs.class_tab import create_class_tab

def criar_dashboard_admin(root):
    # Limpa tela
    for widget in root.winfo_children():
        widget.destroy()

    # Container principal
    container = ctk.CTkFrame(root, corner_radius=15)
    container.pack(pady=20, padx=40, fill="both", expand=True)

    titulo = ctk.CTkLabel(container, text="Dashboard do Admin", font=ctk.CTkFont(size=22, weight="bold"))
    titulo.pack(pady=20)

    # Tabview principal
    tabview = ctk.CTkTabview(container, height=600)
    tabview.pack(pady=10, fill="both", expand=True)

    # Criar abas
    tabview.add("Administradores")
    tabview.add("Alunos")
    tabview.add("Professores")
    tabview.add("Cursos")
    tabview.add("Disciplinas")
    tabview.add("Turmas")

    # Criar conteúdo das abas
    create_admin_tab(tabview.tab("Administradores"))
    create_student_tab(tabview.tab("Alunos"))
    create_professor_tab(tabview.tab("Professores"))
    create_course_tab(tabview.tab("Cursos"))
    create_discipline_tab(tabview.tab("Disciplinas"))
    create_class_tab(tabview.tab("Turmas"))