import customtkinter as ctk
from tkinter import ttk

class CustomTable(ttk.Treeview):
    def __init__(self, parent, columns, column_widths=None):
        super().__init__(parent, columns=columns, show='headings', selectmode='browse')

        mode = ctk.get_appearance_mode()
        theme = ctk.ThemeManager.theme

        # Cores adaptadas ao tema escuro
        base_bg = theme["CTkFrame"]["fg_color"][1 if mode == "Dark" else 0]
        entry_bg = theme["CTkEntry"]["fg_color"][1 if mode == "Dark" else 0]
        button_fg = theme["CTkButton"]["fg_color"][1 if mode == "Dark" else 0]
        text_color = theme["CTkLabel"]["text_color"][1 if mode == "Dark" else 0]
        hover_color = theme["CTkButton"]["hover_color"][1 if mode == "Dark" else 0]

        # Tons intermediários para zebra
        zebra_1 = entry_bg
        zebra_2 = self._mix_colors(entry_bg, "#202020", 0.15)

        # Estilo base
        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Custom.Treeview",
            background=entry_bg,
            fieldbackground=entry_bg,
            foreground=text_color,
            rowheight=30,
            borderwidth=0,
            relief="flat",
            font=('Segoe UI', 11)
        )

        # Mapeia seleção
        style.map(
            "Custom.Treeview",
            background=[("selected", button_fg)],
            foreground=[("selected", "white")]
        )

        # Cabeçalhos com cor próxima das abas
        style.configure(
            "Custom.Treeview.Heading",
            background=hover_color,
            foreground="white",
            font=('Segoe UI', 10, 'bold'),
            borderwidth=0,
            relief="flat"
        )

        style.map("Custom.Treeview.Heading",
                  background=[("active", button_fg)],
                  foreground=[("active", "white")])

        # Configura colunas
        for idx, col in enumerate(columns):
            width = column_widths[idx] if column_widths else 150
            self.heading(col, text=col.title())
            self.column(col, width=width, anchor="center")

        self.configure(style="Custom.Treeview")

        # Aplica zebra (linhas alternadas)
        self.tag_configure("oddrow", background=zebra_1)
        self.tag_configure("evenrow", background=zebra_2)

    def insert(self, parent, index, iid=None, **kw):
        """Insere linha com zebra automática"""
        children = self.get_children()
        row_tag = "evenrow" if len(children) % 2 == 0 else "oddrow"
        if "tags" in kw:
            kw["tags"].append(row_tag)
        else:
            kw["tags"] = (row_tag,)
        return super().insert(parent, index, iid=iid, **kw)

    def clear(self):
        for item in self.get_children():
            self.delete(item)

    def _mix_colors(self, c1, c2, ratio=0.5):
        """Mistura duas cores hex (ex: '#202020', '#404040')"""
        c1, c2 = c1.lstrip("#"), c2.lstrip("#")
        rgb1 = tuple(int(c1[i:i+2], 16) for i in (0, 2, 4))
        rgb2 = tuple(int(c2[i:i+2], 16) for i in (0, 2, 4))
        mixed = tuple(int(rgb1[i]*(1-ratio) + rgb2[i]*ratio) for i in range(3))
        return f"#{mixed[0]:02x}{mixed[1]:02x}{mixed[2]:02x}"