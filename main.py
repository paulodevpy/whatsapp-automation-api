"""
WhatsApp Sender - Ponto de Entrada
"""
import sys
from pathlib import Path

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent))

from src.gui.app import WhatsAppSenderApp


def main():
    """Inicia a aplicacao"""
    app = WhatsAppSenderApp()
    app.run()


if __name__ == "__main__":
    main()