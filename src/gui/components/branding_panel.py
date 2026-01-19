"""
Componente de branding e créditos
"""
import customtkinter as ctk
from tkinter import messagebox
import webbrowser

from src.gui.styles import Colors, Fonts, Branding


class BrandingPanel(ctk.CTkFrame):
    """Painel de branding com créditos do desenvolvedor"""

    def __init__(self, master):
        super().__init__(master, fg_color=Colors.CARD_BACKGROUND, corner_radius=15)
        self._create_branding()

    def _create_branding(self):
        """Cria elementos de branding"""
        # Container principal com gradiente visual
        main_container = ctk.CTkFrame(
            self,
            fg_color="transparent",
            corner_radius=10
        )
        main_container.pack(fill="x", padx=15, pady=10)

        # Título com arte ASCII melhorada
        title_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        title_frame.pack(fill="x", pady=(5, 10))

        # Arte ASCII moderna e estilizada
        ascii_art = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              🚀  WHATSAPP SENDER PRO  🚀                     ║
║                                                              ║
║           ┌─────────────────────────────────────────┐        ║
║           │     💬  Mensagens em Massa via WhatsApp    │        ║
║           └─────────────────────────────────────────┘        ║
║                                                              ║
║           ✨  Desenvolvido com ❤️  por Paulo Dev  ✨         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """

        title_label = ctk.CTkLabel(
            title_frame,
            text=ascii_art,
            font=ctk.CTkFont(family=Fonts.FAMILY_MONO, size=9, weight=Fonts.WEIGHT_BOLD),
            text_color=Colors.PRIMARY,
            justify="center"
        )
        title_label.pack(pady=(0, 8))

        # Informações do desenvolvedor em layout horizontal
        dev_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        dev_frame.pack(fill="x", pady=(0, 8))

        # Container para informações do dev
        info_container = ctk.CTkFrame(dev_frame, fg_color=Colors.SURFACE, corner_radius=8)
        info_container.pack(fill="x", padx=10)

        # Nome do desenvolvedor
        dev_name = ctk.CTkLabel(
            info_container,
            text=f"👨‍💻 {Branding.DEVELOPER_NAME}",
            font=ctk.CTkFont(size=Fonts.SIZE_MEDIUM, weight=Fonts.WEIGHT_BOLD),
            text_color=Colors.TEXT_PRIMARY
        )
        dev_name.pack(pady=(10, 5))

        # Contatos em linha
        contacts_frame = ctk.CTkFrame(info_container, fg_color="transparent")
        contacts_frame.pack(fill="x", padx=10, pady=(0, 10))

        # GitHub
        github_label = ctk.CTkLabel(
            contacts_frame,
            text=f"🐙 {Branding.DEVELOPER_TAG}",
            font=ctk.CTkFont(size=Fonts.SIZE_NORMAL),
            text_color=Colors.ACCENT_BLUE,
            cursor="hand2"
        )
        github_label.pack(side="left", padx=(0, 15))
        github_label.bind("<Button-1>", lambda e: self._open_github())

        # Separador
        separator = ctk.CTkLabel(
            contacts_frame,
            text="•",
            font=ctk.CTkFont(size=Fonts.SIZE_NORMAL),
            text_color=Colors.TEXT_MUTED
        )
        separator.pack(side="left", padx=5)

        # Email
        email_label = ctk.CTkLabel(
            contacts_frame,
            text=f"📧 {Branding.DEVELOPER_EMAIL}",
            font=ctk.CTkFont(size=Fonts.SIZE_NORMAL),
            text_color=Colors.ACCENT_PURPLE,
            cursor="hand2"
        )
        email_label.pack(side="left", padx=(5, 0))
        email_label.bind("<Button-1>", lambda e: self._open_email())

        # Versão e informações adicionais
        version_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        version_frame.pack(fill="x", padx=10, pady=(5, 10))

        # Container da versão
        version_container = ctk.CTkFrame(version_frame, fg_color=Colors.SURFACE_LIGHT, corner_radius=6)
        version_container.pack(fill="x")

        version_text = f"📅 {Branding.VERSION} • {Branding.RELEASE_DATE}"
        version_label = ctk.CTkLabel(
            version_container,
            text=version_text,
            font=ctk.CTkFont(size=Fonts.SIZE_SMALL),
            text_color=Colors.TEXT_SECONDARY
        )
        version_label.pack(side="left", padx=10, pady=5)

        # Botão de informações
        info_button = ctk.CTkButton(
            version_container,
            text="ℹ️ Sobre",
            width=70,
            height=25,
            font=ctk.CTkFont(size=Fonts.SIZE_SMALL),
            fg_color=Colors.PRIMARY,
            hover_color=Colors.PRIMARY_DARK,
            command=self._show_about
        )
        info_button.pack(side="right", padx=10, pady=5)

    def _open_github(self):
        """Abre perfil do GitHub"""
        webbrowser.open("https://github.com/paulodevpy")

    def _open_email(self):
        """Abre cliente de email"""
        webbrowser.open("mailto:paulodevpy@gmail.com")

    def _show_about(self):
        """Mostra diálogo sobre"""
        about_text = f"""
🚀 {Branding.APP_NAME}

Uma aplicação desktop completa para envio de mensagens
em massa via WhatsApp Web com interface moderna e
inteligente.

✨ Funcionalidades Principais:
• 💬 Envio personalizado com variáveis dinâmicas
• 🎨 Interface responsiva e moderna com tema dark
• 📊 Suporte completo a Excel (.xlsx, .xls) e CSV
• 📈 Monitoramento em tempo real com barra de progresso
• 🤖 Gerenciamento automático do ChromeDriver
• 🖼️ Suporte ao envio de imagens
• 📱 Validação automática de números brasileiros

👨‍💻 Desenvolvido por {Branding.DEVELOPER_NAME}
🐙 {Branding.DEVELOPER_TAG}
📧 {Branding.DEVELOPER_EMAIL}

📅 {Branding.RELEASE_DATE} - Versão {Branding.VERSION}

⭐ Agradecimentos especiais ao ecossistema Python e
às bibliotecas open source que tornam isso possível!
        """

        messagebox.showinfo(f"Sobre - {Branding.APP_NAME}", about_text.strip())