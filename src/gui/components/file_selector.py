"""
Componente de selecao de arquivos
"""
import customtkinter as ctk
from tkinter import filedialog
from typing import Callable, Optional
from pathlib import Path

from src.gui.styles import Colors, Fonts


class FileSelector(ctk.CTkFrame):
    """Componente para selecao de arquivo"""
    
    def __init__(
        self,
        master,
        label: str,
        filetypes: list,
        on_file_selected: Optional[Callable] = None,
        **kwargs
    ):
        super().__init__(master, fg_color=Colors.SURFACE, corner_radius=8, **kwargs)
        
        self._filetypes = filetypes
        self._on_file_selected = on_file_selected
        self._file_path: Optional[str] = None
        
        self._create_widgets(label)
    
    def _create_widgets(self, label: str):
        """Cria widgets do componente"""
        # Label
        self._label = ctk.CTkLabel(
            self,
            text=label,
            font=(Fonts.FAMILY, Fonts.SIZE_NORMAL, "bold"),
            text_color=Colors.TEXT_PRIMARY
        )
        self._label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Frame para input e botao
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Entry para mostrar caminho
        self._entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Nenhum arquivo selecionado",
            state="disabled",
            font=(Fonts.FAMILY, Fonts.SIZE_SMALL),
            fg_color=Colors.SURFACE_LIGHT,
            text_color=Colors.TEXT_SECONDARY
        )
        self._entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Botao selecionar
        self._btn_select = ctk.CTkButton(
            input_frame,
            text="Selecionar",
            command=self._select_file,
            fg_color=Colors.PRIMARY_DARK,
            hover_color=Colors.PRIMARY,
            font=(Fonts.FAMILY, Fonts.SIZE_SMALL),
            width=100
        )
        self._btn_select.pack(side="right")
        
        # Label de status
        self._status_label = ctk.CTkLabel(
            self,
            text="",
            font=(Fonts.FAMILY, Fonts.SIZE_SMALL),
            text_color=Colors.TEXT_SECONDARY
        )
        self._status_label.pack(anchor="w", padx=10, pady=(0, 5))
    
    def _select_file(self):
        """Abre dialogo de selecao de arquivo"""
        file_path = filedialog.askopenfilename(filetypes=self._filetypes)
        
        if file_path:
            self._file_path = file_path
            
            # Atualiza entry
            self._entry.configure(state="normal")
            self._entry.delete(0, "end")
            self._entry.insert(0, Path(file_path).name)
            self._entry.configure(state="disabled")
            
            # Callback
            if self._on_file_selected:
                self._on_file_selected(file_path)
    
    def set_status(self, text: str, is_error: bool = False):
        """Define texto de status"""
        color = Colors.ERROR if is_error else Colors.SUCCESS
        self._status_label.configure(text=text, text_color=color)
    
    def clear_status(self):
        """Limpa status"""
        self._status_label.configure(text="")
    
    @property
    def file_path(self) -> Optional[str]:
        return self._file_path
    
    def clear(self):
        """Limpa selecao"""
        self._file_path = None
        self._entry.configure(state="normal")
        self._entry.delete(0, "end")
        self._entry.configure(state="disabled")
        self.clear_status()