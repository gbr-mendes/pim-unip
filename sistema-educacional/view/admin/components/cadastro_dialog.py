import customtkinter as ctk
from .feedback import mostrar_feedback

def criar_janela_cadastro(parent, titulo, callback_cadastro, campos):
    """Cria uma janela de cadastro sobreposta"""
    window = ctk.CTkToplevel(parent)
    window.title(titulo)
    window.geometry("400x600")
    window.transient(parent)
    window.grab_set()
    
    frame = ctk.CTkFrame(window)
    frame.pack(padx=20, pady=20, fill="both", expand=True)
    
    ctk.CTkLabel(frame, text=titulo, font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
    
    entries = {}
    dependent_fields = {}
    
    for campo in campos:
        if campo.get('type') == 'select':
            # Criar label para o select
            ctk.CTkLabel(frame, text=campo['label']).pack(fill="x", padx=20, pady=(10,0))
            # Criar combobox
            combobox = ctk.CTkComboBox(frame, values=[f"{item['id']} - {item['nome']}" for item in campo['options']])
            combobox.pack(fill="x", padx=20, pady=(0,10))
            
            if campo.get('default'):
                combobox.set(campo['default'])
                
            entries[campo['name']] = combobox
            
            # Se este campo tem dependentes, configurar o callback
            if campo.get('dependents'):
                dependent_fields[campo['name']] = campo['dependents']
                
                def on_combobox_select(choice, name=campo['name']):
                    update_dependent_fields(name)
                
                combobox.configure(command=on_combobox_select)
                
        else:
            # Campo normal de texto
            entry = ctk.CTkEntry(frame, placeholder_text=campo['placeholder'])
            entry.pack(fill="x", padx=20, pady=10)
            if campo.get('password', False):
                entry.configure(show="*")
            entries[campo['name']] = entry
    
    def update_dependent_fields(field_name):
        if field_name not in dependent_fields:
            return
            
        selected = entries[field_name].get()
        if not selected:
            return
            
        selected_id = selected.split(' - ')[0]
        
        for dep_field in dependent_fields[field_name]:
            dependent_combobox = entries[dep_field['name']]
            # Atualizar opções baseado no valor selecionado
            new_options = dep_field['update_options'](selected_id)
            if new_options:
                # Criar lista de strings formatadas para as opções
                option_strings = [f"{item['id']} - {item['nome']}" for item in new_options]
                # Atualizar valores do combobox
                dependent_combobox.configure(values=option_strings)
                # Se houver opções, selecionar a primeira
                if option_strings:
                    dependent_combobox.set(option_strings[0])
                else:
                    dependent_combobox.set("")
            else:
                dependent_combobox.configure(values=[])
                dependent_combobox.set("")
    
    def submit():
        valores = {}
        for name, widget in entries.items():
            if isinstance(widget, ctk.CTkComboBox):
                # Pegar apenas o ID do item selecionado (antes do hífen)
                valor = widget.get().split(' - ')[0] if widget.get() else None
                valores[name] = valor
            else:
                valores[name] = widget.get()
        
        response = callback_cadastro(**valores)
        if response["status"] == "ok":
            window.destroy()
        else:
            mostrar_feedback(frame, response["message"], "error")
    
    ctk.CTkButton(frame, text="Cadastrar", command=submit).pack(pady=20)
    ctk.CTkButton(frame, text="Voltar", command=window.destroy).pack(pady=5)