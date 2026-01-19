"""
Painel de progresso e logs
"""
import customtkinter as ctk
from datetime import datetime

from src.gui.styles import Colors, Fonts


class ProgressPanel(ctk.CTkFrame):
    """Painel de progresso com logs e estatisticas"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=Colors.SURFACE, corner_radius=8, **kwargs)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Cria widgets do componente"""
        # Label
        label = ctk.CTkLabel(
            self,
            text="Progresso",
            font=(Fonts.FAMILY, Fonts.SIZE_NORMAL, "bold"),
            text_color=Colors.TEXT
        )
        label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Barra de progresso
        self._progress_bar = ctk.CTkProgressBar(
            self,
            fg_color=Colors.SURFACE_LIGHT,
            progress_color=Colors.PRIMARY
        )
        self._progress_bar.pack(fill="x", padx=10, pady=(0, 5))
        self._progress_bar.set(0)
        
        # Label de progresso
        self._progress_label = ctk.CTkLabel(
            self,
            text="0 / 0 (0%)",
            font=(Fonts.FAMILY, Fonts.SIZE_SMALL),
            text_color=Colors.TEXT_SECONDARY
        )
        self._progress_label.pack(anchor="w", padx=10, pady=(0, 10))
        
        # Frame de estatisticas
        stats_frame = ctk.CTkFrame(self, fg_color=Colors.SURFACE_LIGHT, corner_radius=6)
        stats_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Estatisticas
        self._stats_labels = {}
        stats_config = [
            ("sent", "Enviados", Colors.SUCCESS),
            ("failed", "Falhas", Colors.ERROR),
            ("skipped", "Pulados", Colors.WARNING),
            ("invalid", "Invalidos", Colors.INFO),
        ]
        
        for key, text, color in stats_config:
            frame = ctk.CTkFrame(stats_frame, fg_color="transparent")
            frame.pack(side="left", expand=True, padx=10, pady=8)
            
            value_label = ctk.CTkLabel(
                frame,
                text="0",
                font=(Fonts.FAMILY, Fonts.SIZE_LARGE, "bold"),
                text_color=color
            )
            value_label.pack()
            
            text_label = ctk.CTkLabel(
                frame,
                text=text,
                font=(Fonts.FAMILY, Fonts.SIZE_SMALL),
                text_color=Colors.TEXT_SECONDARY
            )
            text_label.pack()
            
            self._stats_labels[key] = value_label
        
        # Log
        log_label = ctk.CTkLabel(
            self,
            text="Log",
            font=(Fonts.FAMILY, Fonts.SIZE_SMALL, "bold"),
            text_color=Colors.TEXT_SECONDARY
        )
        log_label.pack(anchor="w", padx=10, pady=(0, 5))
        
        self._log_box = ctk.CTkTextbox(
            self,
            font=(Fonts.FAMILY, Fonts.SIZE_SMALL),
            fg_color=Colors.SURFACE_LIGHT,
            text_color=Colors.TEXT,
            height=150,
            state="disabled"
        )
        self._log_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))
    
    def update_progress(self, current: int, total: int, percent: float):
        """Atualiza barra de progresso"""
        self._progress_bar.set(percent / 100)
        self._progress_label.configure(text=f"{current} / {total} ({percent:.1f}%)")
    
    def update_stats(self, stats: dict):
        """Atualiza estatisticas"""
        for key, label in self._stats_labels.items():
            if key in stats:
                label.configure(text=str(stats[key]))
    
    def add_log(self, message: str):
        """Adiciona mensagem ao log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        self._log_box.configure(state="normal")
        self._log_box.insert("end", log_message)
        self._log_box.see("end")
        self._log_box.configure(state="disabled")
    
    def clear(self):
        """Limpa progresso e logs"""
        self._progress_bar.set(0)
        self._progress_label.configure(text="0 / 0 (0%)")
        
        for label in self._stats_labels.values():
            label.configure(text="0")
        
        self._log_box.configure(state="normal")
        self._log_box.delete("1.0", "end")
        self._log_box.configure(state="disabled")