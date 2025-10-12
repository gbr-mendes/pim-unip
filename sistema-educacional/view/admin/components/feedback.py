import customtkinter as ctk

def mostrar_feedback(frame, mensagem, tipo="error", row=None):
    """Mostra feedback ao usuário com cor apropriada"""
    # Remove feedback anterior se existir
    for widget in frame.winfo_children():
        if isinstance(widget, ctk.CTkLabel) and hasattr(widget, 'feedback_label'):
            widget.destroy()
    
    # Configura cor baseada no tipo
    cor = "#FF4444" if tipo == "error" else "#4CAF50"
    
    # Cria label de feedback
    feedback = ctk.CTkLabel(frame, text=mensagem, text_color=cor)
    feedback.feedback_label = True  # marca como label de feedback
    
    if row is not None:
        feedback.grid(row=row, column=0, columnspan=2, pady=(5, 10))
    else:
        feedback.pack(pady=(5, 10))