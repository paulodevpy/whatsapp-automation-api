"""
Aplicacao principal - Janela principal da GUI
"""
import customtkinter as ctk
import threading
from tkinter import messagebox
from typing import Optional, List

from src.gui.styles import Colors, Fonts, Dimensions
from src.gui.components import (
    FileSelector,
    MessageEditor,
    PreviewPanel,
    ProgressPanel,
    ControlPanel,
    BrandingPanel
)
from src.models import Contact, MessageTemplate
from src.services import SpreadsheetService, WhatsAppService
from src.config import config


class WhatsAppSenderApp:
    """Aplicacao principal do WhatsApp Sender"""
    
    def __init__(self):
        self._setup_window()
        self._init_services()
        self._init_state()
        self._create_layout()
    
    def _setup_window(self):
        """Configura janela principal"""
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        
        self._root = ctk.CTk()
        self._root.title("🚀 WhatsApp Sender Pro - by @paulodevpy")
        self._root.geometry(f"{Dimensions.WINDOW_WIDTH}x{Dimensions.WINDOW_HEIGHT}")
        self._root.minsize(800, 600)
        self._root.resizable(True, True)
        
        # Centraliza janela
        self._root.update_idletasks()
        x = (self._root.winfo_screenwidth() - Dimensions.WINDOW_WIDTH) // 2
        y = (self._root.winfo_screenheight() - Dimensions.WINDOW_HEIGHT) // 2
        self._root.geometry(f"+{x}+{y}")
        
        # Configura cor de fundo
        self._root.configure(fg_color=Colors.BACKGROUND)
    
    def _init_services(self):
        """Inicializa servicos"""
        self._spreadsheet_service = SpreadsheetService()
        self._whatsapp_service: Optional[WhatsAppService] = None
    
    def _init_state(self):
        """Inicializa estado da aplicacao"""
        self._contacts: List[Contact] = []
        self._image_path: Optional[str] = None
        self._is_running = False
    
    def _create_layout(self):
        """Cria layout da interface"""
        # Branding Panel (no topo)
        self._branding_panel = BrandingPanel(self._root)
        self._branding_panel.pack(fill="x", padx=10, pady=(10, 5))

        # Header
        self._create_header()

        # Container principal
        main_container = ctk.CTkScrollableFrame(self._root, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Coluna esquerda (configuracoes)
        left_column = ctk.CTkFrame(main_container, fg_color="transparent")
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Coluna direita (progresso)
        right_column = ctk.CTkFrame(main_container, fg_color="transparent")
        right_column.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # === Coluna Esquerda ===
        
        # Seletor de planilha
        self._file_selector = FileSelector(
            left_column,
            label="Planilha de Contatos",
            filetypes=[
                ("Planilhas", "*.xlsx *.xls *.csv"),
                ("Excel", "*.xlsx *.xls"),
                ("CSV", "*.csv")
            ],
            on_file_selected=self._on_spreadsheet_selected
        )
        self._file_selector.pack(fill="x", pady=(0, 10))
        
        # Seletor de imagem
        self._image_selector = FileSelector(
            left_column,
            label="Imagem (Opcional)",
            filetypes=[
                ("Imagens", "*.png *.jpg *.jpeg *.gif *.webp"),
                ("PNG", "*.png"),
                ("JPEG", "*.jpg *.jpeg")
            ],
            on_file_selected=self._on_image_selected
        )
        self._image_selector.pack(fill="x", pady=(0, 10))
        
        # Editor de mensagem
        self._message_editor = MessageEditor(
            left_column,
            on_text_changed=self._on_message_changed
        )
        self._message_editor.pack(fill="both", expand=True, pady=(0, 10))
        
        # Preview
        self._preview_panel = PreviewPanel(left_column)
        self._preview_panel.pack(fill="x", pady=(0, 10))
        
        # Controles
        self._control_panel = ControlPanel(
            left_column,
            on_start=self._on_start,
            on_stop=self._on_stop,
            on_clear=self._on_clear,
            on_about=self._show_about
        )
        self._control_panel.pack(fill="x")
        self._control_panel.set_start_enabled(False)
        
        # === Coluna Direita ===
        
        # Painel de progresso
        self._progress_panel = ProgressPanel(right_column)
        self._progress_panel.pack(fill="both", expand=True)
    
    def _create_header(self):
        """Cria header da aplicacao"""
        header = ctk.CTkFrame(self._root, fg_color=Colors.SURFACE, height=60)
        header.pack(fill="x", padx=20, pady=20)
        header.pack_propagate(False)
        
        # Titulo
        title = ctk.CTkLabel(
            header,
            text="WhatsApp Sender",
            font=(Fonts.FAMILY, Fonts.SIZE_TITLE, "bold"),
            text_color=Colors.PRIMARY
        )
        title.pack(side="left", padx=20, pady=15)
        
        # Subtitulo
        subtitle = ctk.CTkLabel(
            header,
            text="Envio de mensagens em massa via WhatsApp Web",
            font=(Fonts.FAMILY, Fonts.SIZE_SMALL),
            text_color=Colors.TEXT_SECONDARY
        )
        subtitle.pack(side="left", pady=15)
    
    # === Event Handlers ===
    
    def _on_spreadsheet_selected(self, file_path: str):
        """Callback quando planilha e selecionada"""
        success, message = self._spreadsheet_service.load(file_path)
        
        if success:
            self._contacts = self._spreadsheet_service.get_contacts()
            self._file_selector.set_status(f"{len(self._contacts)} contatos encontrados")
            
            # Atualiza wildcards baseados nas colunas
            columns = self._spreadsheet_service.get_columns()
            wildcards = [f"{{{col}}}" for col in columns]
            
            # Adiciona variaveis derivadas se houver coluna de nome
            name_columns = ['nome_completo', 'nome', 'name', 'full_name']
            if any(col in name_columns for col in columns):
                wildcards.extend(['{primeiro_nome}', '{ultimo_nome}'])
            
            self._message_editor.update_wildcards(wildcards)
            
            self._update_preview()
            self._check_can_start()
            self._progress_panel.add_log(f"Planilha carregada: {len(self._contacts)} contatos")
        else:
            self._file_selector.set_status(message, is_error=True)
            self._contacts = []
            self._control_panel.set_start_enabled(False)
    
    def _on_image_selected(self, file_path: str):
        """Callback quando imagem e selecionada"""
        self._image_path = file_path
        self._image_selector.set_status("Imagem selecionada")
        self._progress_panel.add_log(f"Imagem selecionada")
    
    def _on_message_changed(self, text: str):
        """Callback quando mensagem muda"""
        self._update_preview()
        self._check_can_start()
    
    def _update_preview(self):
        """Atualiza preview da mensagem"""
        text = self._message_editor.get_text()
        template = MessageTemplate(text=text, image_path=self._image_path)
        
        contact = self._contacts[0] if self._contacts else None
        self._preview_panel.update_preview(contact, template)
    
    def _check_can_start(self):
        """Verifica se pode iniciar envio"""
        has_contacts = len(self._contacts) > 0
        has_message = len(self._message_editor.get_text().strip()) > 0
        
        can_start = has_contacts and has_message and not self._is_running
        self._control_panel.set_start_enabled(can_start)
    
    def _on_start(self):
        """Inicia envio de mensagens"""
        if not self._contacts:
            messagebox.showerror("Erro", "Nenhum contato carregado")
            return
        
        message_text = self._message_editor.get_text().strip()
        if not message_text:
            messagebox.showerror("Erro", "Digite uma mensagem")
            return
        
        # Confirmacao
        confirm = messagebox.askyesno(
            "Confirmar Envio",
            f"Deseja enviar mensagens para {len(self._contacts)} contatos?\n\n"
            "O navegador sera aberto. Escaneie o QR Code se necessario."
        )
        
        if not confirm:
            return
        
        # Inicia em thread separada
        self._is_running = True
        self._control_panel.set_running(True)
        self._progress_panel.clear()
        self._progress_panel.add_log("Iniciando envio...")
        
        thread = threading.Thread(target=self._run_send_process, daemon=True)
        thread.start()
    
    def _run_send_process(self):
        """Executa processo de envio (em thread separada)"""
        try:
            # Inicializa servico
            self._whatsapp_service = WhatsAppService()
            
            self._log("Inicializando navegador...")
            if not self._whatsapp_service.initialize():
                self._log("Erro ao inicializar navegador")
                self._finish_send()
                return
            
            self._log("Aguardando login no WhatsApp Web...")
            self._log("Escaneie o QR Code se necessario")
            
            if not self._whatsapp_service.login():
                self._log("Timeout no login. Tente novamente.")
                self._whatsapp_service.close()
                self._finish_send()
                return
            
            self._log("Login realizado com sucesso!")
            
            # Cria template
            template = MessageTemplate(
                text=self._message_editor.get_text(),
                image_path=self._image_path
            )
            
            # Envia mensagens
            stats = self._whatsapp_service.send_batch(
                contacts=self._contacts,
                template=template,
                progress_callback=self._update_progress,
                log_callback=self._log
            )
            
            # Finaliza
            self._log("-" * 40)
            self._log(f"CONCLUIDO - Enviados: {stats['sent']} | Falhas: {stats['failed']} | Pulados: {stats['skipped']}")
            
            self._root.after(0, lambda: self._progress_panel.update_stats(stats))
            
        except Exception as e:
            self._log(f"Erro: {str(e)}")
        finally:
            if self._whatsapp_service:
                self._whatsapp_service.close()
            self._finish_send()
    
    def _update_progress(self, current: int, total: int, percent: float):
        """Callback de progresso (thread-safe)"""
        self._root.after(0, lambda: self._progress_panel.update_progress(current, total, percent))
    
    def _log(self, message: str):
        """Adiciona log (thread-safe)"""
        self._root.after(0, lambda: self._progress_panel.add_log(message))
    
    def _finish_send(self):
        """Finaliza processo de envio"""
        self._is_running = False
        self._root.after(0, lambda: self._control_panel.set_running(False))
    
    def _on_stop(self):
        """Para envio de mensagens"""
        if self._whatsapp_service:
            self._whatsapp_service.stop()
            self._progress_panel.add_log("Parando envio...")
    
    def _on_clear(self):
        """Limpa todos os campos"""
        self._contacts = []
        self._image_path = None
        
        self._file_selector.clear()
        self._image_selector.clear()
        self._message_editor.clear()
        self._preview_panel.clear()
        self._progress_panel.clear()
        self._control_panel.set_start_enabled(False)
    
    def _show_about(self):
        """Mostra diálogo sobre"""
        from src.gui.components.branding_panel import BrandingPanel
        # Cria uma instância temporária apenas para usar o método _show_about
        temp_panel = BrandingPanel(self._root)
        temp_panel._show_about()
    
    def run(self):
        """Executa a aplicacao"""
        self._root.mainloop()