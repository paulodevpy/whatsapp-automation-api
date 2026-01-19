"""
Componente de edicao de mensagem
"""
import customtkinter as ctk
from typing import Callable, Optional

from src.gui.styles import Colors, Fonts
from src.models import MessageTemplate


class MessageEditor(ctk.CTkFrame):
    """Editor de mensagem com suporte a wildcards"""
    
    def __init__(
        self,
        master,
        on_text_changed: Optional[Callable] = None,
        wildcards: Optional[list] = None,
        **kwargs
    ):
        super().__init__(master, fg_color=Colors.SURFACE, corner_radius=8, **kwargs)
        
        self._on_text_changed = on_text_changed
        self._wildcards = wildcards or self._get_default_wildcards()
        self._create_widgets()
    
    def _get_default_wildcards(self) -> list:
        """Retorna wildcards padrao"""
        return ["{data_atual}", "{hora_atual}", "{saudacao}"]
    
    def update_wildcards(self, wildcards: list):
        """Atualiza lista de wildcards"""
        self._wildcards = wildcards + self._get_default_wildcards()
        self._refresh_wildcard_buttons()
    
    def _refresh_wildcard_buttons(self):
        """Atualiza os botoes de wildcards"""
        # Remove botoes existentes (exceto o label)
        for widget in self._wildcards_frame.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                widget.destroy()
        
        # Recria botoes
        for wc in self._wildcards:
            btn = ctk.CTkButton(
                self._wildcards_frame,
                text=wc,
                command=lambda w=wc: self._insert_wildcard(w),
                fg_color=Colors.PRIMARY_DARK,
                hover_color=Colors.PRIMARY,
                font=(Fonts.FAMILY, Fonts.SIZE_SMALL),
                height=28,
                width=120
            )
            btn.pack(side="left", padx=5, pady=8)
    
    def _create_widgets(self):
        """Cria widgets do componente"""
        # Label
        label = ctk.CTkLabel(
            self,
            text="Mensagem",
            font=(Fonts.FAMILY, Fonts.SIZE_NORMAL, "bold"),
            text_color=Colors.TEXT
        )
        label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Frame de wildcards
        self._wildcards_frame = ctk.CTkFrame(self, fg_color=Colors.SURFACE_LIGHT, corner_radius=6)
        self._wildcards_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        wildcards_label = ctk.CTkLabel(
            self._wildcards_frame,
            text="Variaveis disponiveis:",
            font=(Fonts.FAMILY, Fonts.SIZE_SMALL),
            text_color=Colors.TEXT_SECONDARY
        )
        wildcards_label.pack(side="left", padx=10, pady=8)
        
        # Botoes de wildcard
        for wc in self._wildcards:
            btn = ctk.CTkButton(
                self._wildcards_frame,
                text=wc,
                command=lambda w=wc: self._insert_wildcard(w),
                fg_color=Colors.PRIMARY_DARK,
                hover_color=Colors.PRIMARY,
                font=(Fonts.FAMILY, Fonts.SIZE_SMALL),
                height=28,
                width=120
            )
            btn.pack(side="left", padx=5, pady=8)
        
        # Textbox
        self._textbox = ctk.CTkTextbox(
            self,
            font=(Fonts.FAMILY, Fonts.SIZE_NORMAL),
            fg_color=Colors.SURFACE_LIGHT,
            text_color=Colors.TEXT,
            height=150
        )
        self._textbox.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Bind para detectar mudancas
        self._textbox.bind("<KeyRelease>", self._on_key_release)
    
    def _insert_wildcard(self, wildcard: str):
        """Insere wildcard na posicao do cursor"""
        self._textbox.insert("insert", wildcard)
        self._textbox.focus()
        self._notify_change()
    
    def _on_key_release(self, event):
        """Callback quando tecla e liberada"""
        self._notify_change()
    
    def _notify_change(self):
        """Notifica mudanca no texto"""
        if self._on_text_changed:
            self._on_text_changed(self.get_text())
    
    def get_text(self) -> str:
        """Retorna texto da mensagem"""
        return self._textbox.get("1.0", "end-1c")
    
    def set_text(self, text: str):
        """Define texto da mensagem"""
        self._textbox.delete("1.0", "end")
        self._textbox.insert("1.0", text)
    
    def clear(self):
        """Limpa o editor"""
        self._textbox.delete("1.0", "end")