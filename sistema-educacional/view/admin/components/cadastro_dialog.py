import customtkinter as ctk
from .feedback import mostrar_feedback
from .multi_select import MultiSelectComboBox

def criar_janela_cadastro(parent, titulo, callback_cadastro, campos):
    """Cria uma janela de cadastro sobreposta"""
    window = ctk.CTkToplevel(parent)
    window.title(titulo)
    window.geometry("400x700")
    window.transient(parent)
    window.grab_set()
    
    frame = ctk.CTkFrame(window)
    frame.pack(padx=20, pady=20, fill="both", expand=True)
    frame.pack_propagate(False)
    
    ctk.CTkLabel(frame, text=titulo, font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
    
    entries = {}
    dependent_fields = {}
    
    for campo in campos:
        # Criar frame para cada campo
        field_frame = ctk.CTkFrame(frame, fg_color="transparent")
        field_frame.pack(fill="x", padx=20, pady=2)
        
        # Label comum para todos os tipos de campo
        if campo.get('label'):
            ctk.CTkLabel(field_frame, text=campo['label']).pack(anchor="w")
        
        if campo.get('type') == 'select':
            if campo.get('multi_select', False):
                # Criar multi-select combobox
                widget = MultiSelectComboBox(field_frame)
                widget.configure(values=[f"{item['id']} - {item['nome']}" for item in campo['options']])
            else:
                # Criar combobox padrão
                widget = ctk.CTkComboBox(
                    field_frame, 
                    values=[f"{item['id']} - {item['nome']}" for item in campo['options']],
                    state="readonly"
                )
                if campo.get('default'):
                    widget.set(campo['default'])
            
            widget.pack(fill="x", pady=5)
            entries[campo['name']] = widget
            
            # Se este campo tem dependentes, configurar o callback
            if campo.get('dependents'):
                dependent_fields[campo['name']] = campo['dependents']
                
                def on_select(choice=None, name=campo['name']):
                    update_dependent_fields(name)
                
                if isinstance(widget, MultiSelectComboBox):
                    widget.configure(callback=on_select)
                else:
                    widget.configure(command=on_select)
                
        else:
            # Campo normal de texto
            widget = ctk.CTkEntry(field_frame, placeholder_text=campo.get('placeholder', ''))
            widget.pack(fill="x", pady=5)
            if campo.get('password', False):
                widget.configure(show="*")
            entries[campo['name']] = widget
    
    def update_dependent_fields(field_name):
        if field_name not in dependent_fields:
            return
            
        widget = entries[field_name]
        if isinstance(widget, MultiSelectComboBox):
            selected_values = widget.get()
            if not selected_values:
                selected_id = None
            else:
                # Use o primeiro valor selecionado para atualizar dependentes
                selected_id = selected_values[0].split(' - ')[0]
        else:
            selected = widget.get()
            if not selected:
                selected_id = None
            else:
                selected_id = selected.split(' - ')[0]
            
        if not selected_id:
            return
            
        for dep_field in dependent_fields[field_name]:
            dependent_widget = entries[dep_field['name']]
            # Atualizar opções baseado no valor selecionado
            new_options = dep_field['update_options'](selected_id)
            if new_options:
                # Criar lista de strings formatadas para as opções
                option_strings = [f"{item['id']} - {item['nome']}" for item in new_options]
                # Atualizar valores do widget
                if isinstance(dependent_widget, MultiSelectComboBox):
                    dependent_widget.configure(values=option_strings)
                    dependent_widget.clear()
                else:
                    dependent_widget.configure(values=option_strings)
                    if option_strings:
                        dependent_widget.set(option_strings[0])
                    else:
                        dependent_widget.set("")
            else:
                if isinstance(dependent_widget, MultiSelectComboBox):
                    dependent_widget.configure(values=[])
                    dependent_widget.clear()
                else:
                    dependent_widget.configure(values=[])
                    dependent_widget.set("")
    
    def submit():
        valores = {}
        for name, widget in entries.items():
            if isinstance(widget, MultiSelectComboBox):
                # Para multi-select, retorna lista de IDs
                valores[name] = [v.split(' - ')[0] for v in widget.get()] if widget.get() else []
            elif isinstance(widget, ctk.CTkComboBox):
                # Para combobox normal, retorna um único ID
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