"""
Estilos e temas da interface
"""
from dataclasses import dataclass


@dataclass
class Colors:
    """Paleta de cores"""
    # Cores principais (WhatsApp)
    PRIMARY = "#25D366"      # Verde WhatsApp
    PRIMARY_DARK = "#128C7E"
    PRIMARY_LIGHT = "#DCF8C6"
    PRIMARY_GRADIENT_START = "#25D366"
    PRIMARY_GRADIENT_END = "#128C7E"

    # Fundo e superfícies
    BACKGROUND = "#0f0f23"   # Fundo escuro elegante
    SURFACE = "#1a1a2e"      # Superfície principal
    SURFACE_LIGHT = "#16213e" # Superfície clara
    CARD_BACKGROUND = "#1e1e2f" # Fundo dos cards

    # Texto
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#b0b0b0"
    TEXT_MUTED = "#808080"

    # Estados
    SUCCESS = "#4ade80"
    ERROR = "#f87171"
    WARNING = "#fbbf24"
    INFO = "#60a5fa"

    # Accent colors para branding
    ACCENT_BLUE = "#3b82f6"
    ACCENT_PURPLE = "#8b5cf6"
    ACCENT_PINK = "#ec4899"

    # Gradientes para efeitos visuais
    GRADIENT_DARK = "#0f0f23"
    GRADIENT_LIGHT = "#1a1a2e"


@dataclass
class Fonts:
    """Configuracoes de fonte"""
    FAMILY = "Segoe UI"
    FAMILY_MONO = "Consolas"

    SIZE_SMALL = 10
    SIZE_NORMAL = 12
    SIZE_MEDIUM = 14
    SIZE_LARGE = 16
    SIZE_TITLE = 22
    SIZE_HEADER = 18

    # Pesos
    WEIGHT_NORMAL = "normal"
    WEIGHT_BOLD = "bold"

    # Estilos específicos
    TITLE = None  # Será definido dinamicamente
    BODY = None   # Será definido dinamicamente
    CAPTION = None # Será definido dinamicamente


@dataclass
class Branding:
    """Constantes de branding"""
    DEVELOPER_NAME = "Paulo Dev"
    DEVELOPER_TAG = "@paulodevpy"
    DEVELOPER_EMAIL = "paulodevpy@gmail.com"
    APP_NAME = "WhatsApp Sender Pro"
    VERSION = "1.0.0"
    RELEASE_DATE = "Janeiro 2026"

    # URLs
    GITHUB_URL = "https://github.com/paulodevpy"
    EMAIL_URL = f"mailto:{DEVELOPER_EMAIL}"


@dataclass
class Dimensions:
    """Dimensoes padrao"""
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 700
    PADDING = 15
    BORDER_RADIUS = 8