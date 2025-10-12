import customtkinter as ctk

class MultiSelectComboBox(ctk.CTkFrame):
    def __init__(self, parent, placeholder_text="Selecione...", values=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.values = values or []
        self.selected = set()
        self.placeholder_text = placeholder_text
        self.is_open = False

        # Campo visual (exibe placeholder ou seleções)
        self.display = ctk.CTkEntry(
            self,
            placeholder_text=self.placeholder_text,
            state="readonly",
            text_color=("gray70", "gray80"),
            fg_color=("gray90", "gray20"),
            corner_radius=8
        )
        self.display.pack(fill="x", pady=(0, 4))
        self.display.bind("<Button-1>", self.toggle_dropdown)

        # Frame de opções (scrollable)
        # self.dropdown = ctk.CTkScrollableFrame(self, fg_color=("gray95", "gray15"), height=150)
        self.dropdown = ctk.CTkScrollableFrame(self, fg_color=("gray95", "gray15"), height=60)
        self.checkboxes = []
        for value in self.values:
            cb = ctk.CTkCheckBox(
                self.dropdown,
                text=value,
                command=self._update_selected,
                checkbox_width=18,
                checkbox_height=18,
                border_width=2
            )
            cb.pack(anchor="w", pady=2)
            self.checkboxes.append(cb)

    def toggle_dropdown(self, event=None):
        """Mostra/oculta a lista suspensa."""
        if self.is_open:
            self.dropdown.pack_forget()
        else:
            self.dropdown.pack(fill="x", pady=(0, 5))
        self.is_open = not self.is_open

    def _update_selected(self):
        """Atualiza lista de selecionados e o texto do campo."""
        self.selected.clear()
        for cb in self.checkboxes:
            if cb.get() == 1:
                self.selected.add(cb.cget("text"))

        if self.selected:
            display_text = ", ".join(sorted(self.selected))
            self.display.configure(placeholder_text="", state="normal")
            self.display.delete(0, "end")
            self.display.insert(0, display_text)
            self.display.configure(state="readonly")
        else:
            self.display.configure(state="normal")
            self.display.delete(0, "end")
            self.display.configure(placeholder_text=self.placeholder_text, state="readonly")

    def get(self):
        """Retorna lista de valores selecionados."""
        return list(self.selected)

    def clear(self):
        """Desmarca todas as opções."""
        for cb in self.checkboxes:
            cb.deselect()
        self.selected.clear()
        self._update_selected()

    def configure(self, values=None, **kwargs):
        """Atualiza opções dinamicamente."""
        super().configure(**kwargs)
        if values is not None:
            self.values = values
            for cb in self.checkboxes:
                cb.destroy()
            self.checkboxes.clear()
            for value in values:
                cb = ctk.CTkCheckBox(
                    self.dropdown,
                    text=value,
                    command=self._update_selected,
                    checkbox_width=18,
                    checkbox_height=18,
                    border_width=2
                )
                cb.pack(anchor="w", pady=2)
                self.checkboxes.append(cb)
