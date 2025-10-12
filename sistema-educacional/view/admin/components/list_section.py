import customtkinter as ctk
from .custom_table import CustomTable

def criar_secao_lista(parent, titulo, colunas, larguras_colunas=None):
    """Cria uma seção com título, tabela e botões"""
    frame = ctk.CTkFrame(parent)
    frame.pack(fill="both", expand=True, padx=10, pady=5)
    
    header = ctk.CTkFrame(frame)
    header.pack(fill="x", pady=5)
    
    ctk.CTkLabel(header, text=titulo, font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", padx=5)
    
    tabela = CustomTable(frame, colunas, larguras_colunas)
    tabela.pack(fill="both", expand=True, padx=5, pady=5)
    
    return frame, tabela