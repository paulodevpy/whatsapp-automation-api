"""
Utilitários para ícones e recursos visuais
"""
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import customtkinter as ctk


class IconUtils:
    """Utilitários para criação de ícones e recursos visuais"""

    @staticmethod
    def create_app_icon(size=(64, 64)):
        """Cria um ícone personalizado para a aplicação"""
        # Cria uma imagem RGBA
        img = Image.new('RGBA', size, (38, 140, 126, 255))  # Verde WhatsApp como fundo
        draw = ImageDraw.Draw(img)

        # Desenha um círculo branco no centro
        center = (size[0] // 2, size[1] // 2)
        radius = min(size) // 3
        draw.ellipse(
            [(center[0] - radius, center[1] - radius),
             (center[0] + radius, center[1] + radius)],
            fill=(255, 255, 255, 255)
        )

        # Desenha um ícone de chat simplificado (balão de fala)
        # Corpo do balão
        bubble_center = (center[0] - 5, center[1] - 5)
        bubble_size = radius - 8
        draw.ellipse(
            [(bubble_center[0] - bubble_size, bubble_center[1] - bubble_size),
             (bubble_center[0] + bubble_size, bubble_center[1] + bubble_size)],
            fill=(38, 140, 126, 255)  # Verde WhatsApp
        )

        # Ponta do balão
        draw.polygon(
            [(bubble_center[0] + bubble_size - 5, bubble_center[1] + bubble_size - 10),
             (bubble_center[0] + bubble_size + 8, bubble_center[1] + bubble_size + 5),
             (bubble_center[0] + bubble_size - 5, bubble_center[1] + bubble_size)],
            fill=(38, 140, 126, 255)
        )

        # Linhas do texto (simulando mensagem)
        line_y = bubble_center[1] - 8
        for i in range(3):
            line_width = bubble_size - 8 if i < 2 else bubble_size - 15
            draw.line(
                [(bubble_center[0] - line_width, line_y),
                 (bubble_center[0] + line_width, line_y)],
                fill=(255, 255, 255, 255),
                width=2
            )
            line_y += 6

        return img

    @staticmethod
    def get_icon_base64():
        """Retorna o ícone como base64 para uso em CTk"""
        icon = IconUtils.create_app_icon((32, 32))

        # Converte para base64
        buffer = BytesIO()
        icon.save(buffer, format='PNG')
        icon_base64 = base64.b64encode(buffer.getvalue()).decode()

        return f"data:image/png;base64,{icon_base64}"

    @staticmethod
    def set_window_icon(window):
        """Define o ícone da janela"""
        try:
            icon = IconUtils.create_app_icon((32, 32))
            # Para CTk, podemos tentar definir o ícone
            # Nota: CTk pode não suportar ícones customizados diretamente
            # Esta é uma implementação básica
            pass
        except Exception:
            # Fallback se não conseguir criar ícone
            pass