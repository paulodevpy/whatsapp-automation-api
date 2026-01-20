"""
Painel de preview da mensagem
"""
import customtkinter as ctk
from typing import Optional

from src.gui.styles import Colors, Fonts
from src.models import Contact, MessageTemplate


class PreviewPanel(ctk.CTkFrame):
    """Painel de preview da mensagem renderizada"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=Colors.SURFACE, corner_radius=8, **kwargs)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Cria widgets do componente"""
        # Label
        label = ctk.CTkLabel(
            self,
            text="Preview",
            font=(Fonts.FAMILY, Fonts.SIZE_NORMAL, "bold"),
            text_color=Colors.TEXT_PRIMARY
        )
        label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Info do contato
        self._contact_label = ctk.CTkLabel(
            self,
            text="Selecione uma planilha para ver o preview",
            font=(Fonts.FAMILY, Fonts.SIZE_SMALL),
            text_color=Colors.TEXT_SECONDARY
        )
        self._contact_label.pack(anchor="w", padx=10, pady=(0, 5))
        
        # Textbox de preview (somente leitura)
        self._preview_box = ctk.CTkTextbox(
            self,
            font=(Fonts.FAMILY, Fonts.SIZE_NORMAL),
            fg_color=Colors.PRIMARY_LIGHT,
            text_color="#000000",
            height=120,
            state="disabled"
        )
        self._preview_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))
    
    def update_preview(self, contact: Optional[Contact], template: MessageTemplate):
        """Atualiza preview com dados do contato"""
        if not contact:
            self._contact_label.configure(text="Nenhum contato disponivel")
            self._set_preview_text("")
            return
        
        self._contact_label.configure(
            text=f"Para: {contact.full_name} | Tel: {contact.phone}"
        )
        
        rendered_message = template.render(contact)
        self._set_preview_text(rendered_message)
    
    def _set_preview_text(self, text: str):
        """Define texto do preview"""
        self._preview_box.configure(state="normal")
        self._preview_box.delete("1.0", "end")
        self._preview_box.insert("1.0", text)
        self._preview_box.configure(state="disabled")
    
    def clear(self):
        """Limpa preview"""
        self._contact_label.configure(text="Selecione uma planilha para ver o preview")
        self._set_preview_text("")