"""
Configuracoes centralizadas da aplicacao
"""
from pathlib import Path
from dataclasses import dataclass


@dataclass
class AppConfig:
    """Configuracoes da aplicacao"""
    
    # Diretorios
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    IMAGES_DIR: Path = BASE_DIR / "images"
    LOGS_DIR: Path = BASE_DIR / "logs"
    CHROME_PROFILE_DIR: Path = BASE_DIR / "chrome_profile"
    
    # Tempos (segundos)
    MIN_DELAY: int = 5
    MAX_DELAY: int = 12
    PAGE_TIMEOUT: int = 15
    MESSAGE_TIMEOUT: int = 20
    
    # Pausas
    PAUSE_AFTER: int = 50
    PAUSE_DURATION: int = 60
    
    # Extensoes suportadas
    SPREADSHEET_EXTENSIONS: tuple = (".xlsx", ".xls", ".csv")
    IMAGE_EXTENSIONS: tuple = (".png", ".jpg", ".jpeg", ".gif", ".webp")
    
    def __post_init__(self):
        """Cria diretorios necessarios"""
        for directory in [self.UPLOAD_DIR, self.IMAGES_DIR, self.LOGS_DIR]:
            directory.mkdir(parents=True, exist_ok=True)


# Instancia global de configuracao
config = AppConfig()