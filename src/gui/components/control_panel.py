"""
Painel de controles
"""
import customtkinter as ctk
from typing import Callable, Optional

from src.gui.styles import Colors, Fonts


class ControlPanel(ctk.CTkFrame):
    """Painel com botoes de controle"""

    def __init__(
        self,
        master,
        on_start: Optional[Callable] = None,
        on_stop: Optional[Callable] = None,
        on_clear: Optional[Callable] = None,
        on_about: Optional[Callable] = None,
        **kwargs
    ):
        super().__init__(master, fg_color="transparent", **kwargs)

        self._on_start = on_start
        self._on_stop = on_stop
        self._on_clear = on_clear
        self._on_about = on_about

        self._create_widgets()
    
    def _create_widgets(self):
        """Cria widgets do componente"""
        # Botao Iniciar
        self._btn_start = ctk.CTkButton(
            self,
            text="Iniciar Envio",
            command=self._handle_start,
            fg_color=Colors.PRIMARY,
            hover_color=Colors.PRIMARY_DARK,
            font=(Fonts.FAMILY, Fonts.SIZE_NORMAL, "bold"),
            height=45,
            width=150
        )
        self._btn_start.pack(side="left", padx=(0, 10))
        
        # Botao Parar
        self._btn_stop = ctk.CTkButton(
            self,
            text="Parar",
            command=self._handle_stop,
            fg_color=Colors.ERROR,
            hover_color="#dc2626",
            font=(Fonts.FAMILY, Fonts.SIZE_NORMAL, "bold"),
            height=45,
            width=100,
            state="disabled"
        )
        self._btn_stop.pack(side="left", padx=(0, 10))
        
        # Botao Limpar
        self._btn_clear = ctk.CTkButton(
            self,
            text="Limpar",
            command=self._handle_clear,
            fg_color=Colors.SURFACE_LIGHT,
            hover_color=Colors.SURFACE,
            font=(Fonts.FAMILY, Fonts.SIZE_NORMAL),
            height=45,
            width=100
        )
        self._btn_clear.pack(side="left", padx=(0, 10))

        # Espaçador
        spacer = ctk.CTkFrame(self, fg_color="transparent", width=20)
        spacer.pack(side="left")

        # Botao Sobre
        self._btn_about = ctk.CTkButton(
            self,
            text="👨‍💻 Sobre",
            command=self._handle_about,
            fg_color=Colors.ACCENT_BLUE,
            hover_color="#2563eb",
            font=(Fonts.FAMILY, Fonts.SIZE_NORMAL, "bold"),
            height=45,
            width=120
        )
        self._btn_about.pack(side="right")
    
    def _handle_start(self):
        if self._on_start:
            self._on_start()
    
    def _handle_stop(self):
        if self._on_stop:
            self._on_stop()
    
    def _handle_clear(self):
        if self._on_clear:
            self._on_clear()
    
    def _handle_about(self):
        if self._on_about:
            self._on_about()
    
    def set_running(self, is_running: bool):
        """Define estado de execucao"""
        if is_running:
            self._btn_start.configure(state="disabled")
            self._btn_stop.configure(state="normal")
            self._btn_clear.configure(state="disabled")
        else:
            self._btn_start.configure(state="normal")
            self._btn_stop.configure(state="disabled")
            self._btn_clear.configure(state="normal")
    
    def set_start_enabled(self, enabled: bool):
        """Habilita/desabilita botao iniciar"""
        state = "normal" if enabled else "disabled"
        self._btn_start.configure(state=state)