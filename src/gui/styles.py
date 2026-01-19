"""
Estilos e temas da interface
"""
from dataclasses import dataclass


@dataclass
class Colors:
    """Paleta de cores"""
    PRIMARY = "#25D366"      # Verde WhatsApp
    PRIMARY_DARK = "#128C7E"
    PRIMARY_LIGHT = "#DCF8C6"
    
    BACKGROUND = "#1a1a2e"
    SURFACE = "#16213e"
    SURFACE_LIGHT = "#0f3460"
    
    TEXT = "#ffffff"
    TEXT_SECONDARY = "#a0a0a0"
    
    SUCCESS = "#4ade80"
    ERROR = "#f87171"
    WARNING = "#fbbf24"
    INFO = "#60a5fa"


@dataclass
class Fonts:
    """Configuracoes de fonte"""
    FAMILY = "Segoe UI"
    SIZE_SMALL = 11
    SIZE_NORMAL = 13
    SIZE_LARGE = 15
    SIZE_TITLE = 20


@dataclass
class Dimensions:
    """Dimensoes padrao"""
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 700
    PADDING = 15
    BORDER_RADIUS = 8