"""
Servico de envio de mensagens via WhatsApp Web
"""
import time
import random
import os
import winreg
import requests
import zipfile
import io
import shutil
from pathlib import Path
from typing import Optional, Callable, List
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

from src.config import config
from src.models import Contact, ContactStatus, MessageTemplate
from src.services.phone_service import PhoneService


class WhatsAppService:
    """Servico de envio de mensagens via WhatsApp Web"""
    
    def __init__(self):
        self._driver: Optional[webdriver.Chrome] = None
        self._is_logged_in: bool = False
        self._messages_sent: int = 0
        self._is_running: bool = False
        self._should_stop: bool = False
    
    def _ensure_chromedriver(self) -> str:
        """Garante que o ChromeDriver esteja disponivel"""
        import sys
        import os

        # Primeiro tenta usar o chromedriver empacotado (PyInstaller)
        if getattr(sys, 'frozen', False):
            # Estamos rodando como executável
            base_path = os.path.dirname(sys.executable)
            driver_path = os.path.join(base_path, "chromedriver.exe")
            if os.path.exists(driver_path):
                try:
                    service = Service(driver_path)
                    options = Options()
                    options.add_argument("--headless")
                    options.add_argument("--no-sandbox")
                    driver = webdriver.Chrome(service=service, options=options)
                    driver.quit()
                    return driver_path
                except Exception as e:
                    print(f"ChromeDriver empacotado falhou: {e}")

        # Tenta o chromedriver na pasta do projeto
        driver_path = Path(__file__).parent.parent.parent / "chromedriver.exe"
        if driver_path.exists():
            try:
                service = Service(str(driver_path))
                options = Options()
                options.add_argument("--headless")
                options.add_argument("--no-sandbox")
                driver = webdriver.Chrome(service=service, options=options)
                driver.quit()
                return str(driver_path)
            except Exception as e:
                print(f"ChromeDriver local falhou: {e}")

        # Último recurso: usa webdriver-manager
        try:
            print("Tentando webdriver-manager...")
            driver_path = ChromeDriverManager().install()
            return driver_path
        except Exception as e:
            print(f"Webdriver-manager falhou: {e}")

        # Se tudo falhar, tenta download manual
        return self._download_chromedriver_manual()
    
    def _download_chromedriver_manual(self) -> str:
        """Download manual do ChromeDriver como último recurso"""
        driver_path = Path(__file__).parent.parent.parent / "chromedriver.exe"
        
        try:
            # Detecta versao do Chrome
            chrome_version = self._get_chrome_version()
            if not chrome_version:
                raise Exception("Google Chrome nao encontrado")
            
            major_version = chrome_version.split(".")[0]
            
            # Obtem versao do ChromeDriver
            api_url = f"https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_{major_version}"
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            driver_version = response.text.strip()
            
            # Baixa o ChromeDriver win32
            download_url = f"https://storage.googleapis.com/chrome-for-testing-public/{driver_version}/win32/chromedriver-win32.zip"
            response = requests.get(download_url, timeout=30)
            response.raise_for_status()
            
            # Extrai
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
                zip_ref.extractall("temp_driver")
            
            # Move o exe
            extracted_exe = Path("temp_driver") / "chromedriver-win32" / "chromedriver.exe"
            extracted_exe.replace(driver_path)
            
            # Limpa temp
            shutil.rmtree("temp_driver", ignore_errors=True)
            
            return str(driver_path)
            
        except Exception as e:
            raise Exception(f"Falha ao baixar ChromeDriver: {e}")
    
    def _get_chrome_version(self) -> Optional[str]:
        """Obtem a versao do Google Chrome via registro"""
        paths = [
            r"SOFTWARE\Google\Chrome\BLBeacon",
            r"SOFTWARE\WOW6432Node\Google\Chrome\BLBeacon",
            r"Software\Google\Chrome\BLBeacon"
        ]
        
        for path in paths:
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
                version, _ = winreg.QueryValueEx(key, "version")
                winreg.CloseKey(key)
                return version
            except FileNotFoundError:
                continue
        return None
    
    def initialize(self) -> bool:
        """Inicializa o driver do navegador"""
        try:
            options = Options()
            
            # Opcoes anti-deteccao
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Perfil persistente
            options.add_argument(f'--user-data-dir={config.CHROME_PROFILE_DIR}')
            options.add_argument('--start-maximized')
            options.add_argument('--disable-notifications')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            
            # Garante que o ChromeDriver esteja disponivel
            driver_exe = self._ensure_chromedriver()
            service = Service(driver_exe)
            self._driver = webdriver.Chrome(service=service, options=options)
            
            # Remove flag webdriver
            self._driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )
            
            return True
            
        except Exception as e:
            print(f"Erro ao inicializar driver: {e}")
            return False
    
    def login(self, timeout: int = 120) -> bool:
        """
        Abre WhatsApp Web e aguarda login
        
        Args:
            timeout: Tempo maximo de espera (segundos)
        """
        if not self._driver:
            return False
        
        self._driver.get("https://web.whatsapp.com")
        
        try:
            WebDriverWait(self._driver, timeout).until(
                EC.presence_of_element_located((
                    By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'
                ))
            )
            self._is_logged_in = True
            return True
            
        except TimeoutException:
            return False
    
    def _check_number_exists(self) -> bool:
        """Verifica se numero tem WhatsApp"""
        print("Verificando se numero tem WhatsApp")
        try:
            # Verifica erro
            try:
                error_elem = self._driver.find_element(By.XPATH, "//div[contains(text(), 'inválido') or contains(text(), 'invalid') or contains(text(), 'não existe') or contains(text(), 'Phone number') or contains(text(), 'número') or contains(text(), 'registrado')]")
                print(f"Erro encontrado: {error_elem.text}")
                return False
            except NoSuchElementException:
                pass
            
            # Verifica se chat abriu
            try:
                WebDriverWait(self._driver, 20).until(
                    EC.presence_of_element_located((
                        By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div/div/div[3]/div[1]/p'
                    ))
                )
                print("Caixa de mensagem encontrada")
                return True
            except TimeoutException:
                print("Timeout aguardando caixa de mensagem")
                return False
                
        except Exception as e:
            print(f"Erro em _check_number_exists: {e}")
            return False
    
    def _open_chat(self, phone: str) -> bool:
        """Abre conversa com numero"""
        print(f"Abrindo chat para: {phone}")
        self._driver.get(f"https://web.whatsapp.com/send?phone={phone}")
        print(f"URL atual: {self._driver.current_url}")
        return self._check_number_exists()
    
    def _send_text(self, message: str) -> bool:
        """Envia mensagem de texto"""
        print(f"Enviando texto: {message}")
        try:
            msg_box = WebDriverWait(self._driver, config.MESSAGE_TIMEOUT).until(
                EC.presence_of_element_located((
                    By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div/div/div[3]/div[1]/p'
                ))
            )
            
            # Digitacao em blocos
            lines = message.split('\n')
            for i, line in enumerate(lines):
                chunk_size = random.randint(15, 25)
                for j in range(0, len(line), chunk_size):
                    msg_box.send_keys(line[j:j + chunk_size])
                    time.sleep(random.uniform(0.03, 0.08))
                
                if i < len(lines) - 1:
                    msg_box.send_keys(Keys.SHIFT + Keys.ENTER)
                    time.sleep(0.05)
            
            time.sleep(0.3)
            msg_box.send_keys(Keys.ENTER)
            return True
            
        except Exception as e:
            print(f"Erro ao enviar texto: {e}")
            return False
    
    def _send_image(self, image_path: str) -> bool:
        """Envia imagem"""
        print(f"Enviando imagem: {image_path}")
        try:
            attach_btn = WebDriverWait(self._driver, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div/div/div[1]/div/span/button/div/div/div[1]/span'
                ))
            )
            attach_btn.click()
            
            # Clica em Fotos e vídeos
            photos_btn = WebDriverWait(self._driver, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH, '//*[@id="app"]/div/div/div[4]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[2]/div[1]/div[2]/span'
                ))
            )
            photos_btn.click()
            
            img_input = WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]'
                ))
            )
            img_input.send_keys(str(Path(image_path).resolve()))
            
            time.sleep(1.0)  # Pequena pausa para upload
            
            # Clica no botão enviar da imagem
            send_img_btn = WebDriverWait(self._driver, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH, '//*[@id="app"]/div/div/div[3]/div/div[3]/div[2]/div/span/div/div/div/div[2]/div/div[2]/div[2]/span/div/div/span'
                ))
            )
            send_img_btn.click()
            return True
            
        except Exception as e:
            print(f"Erro ao enviar imagem: {e}")
            return False
    
    def _wait_between_messages(self):
        """Aguarda entre mensagens"""
        delay = random.uniform(config.MIN_DELAY, config.MAX_DELAY)
        time.sleep(delay)
    
    def _should_pause(self) -> bool:
        """Verifica se deve pausar"""
        return self._messages_sent > 0 and self._messages_sent % config.PAUSE_AFTER == 0
    
    def _take_pause(self):
        """Faz pausa"""
        time.sleep(config.PAUSE_DURATION)
    
    def send_single(
        self,
        contact: Contact,
        template: MessageTemplate
    ) -> ContactStatus:
        """Envia mensagem para um contato"""
        # Valida telefone
        is_valid, error = PhoneService.validate(contact.phone)
        if not is_valid:
            contact.mark_as_invalid(error)
            return ContactStatus.INVALID_PHONE
        
        # Pausa se necessario
        if self._should_pause():
            self._take_pause()
        
        # Abre chat
        if not self._open_chat(contact.phone):
            contact.mark_as_skipped()
            return ContactStatus.SKIPPED
        
        # Envia imagem
        if template.has_image():
            print(f"Template tem imagem: {template.image_path}")
            if not self._send_image(template.image_path):
                contact.mark_as_failed("Falha ao enviar imagem")
                return ContactStatus.FAILED
            time.sleep(0.5)
        
        # Envia texto
        message = template.render(contact)
        print(f"Mensagem renderizada: {message}")
        if not self._send_text(message):
            contact.mark_as_failed("Falha ao enviar texto")
            return ContactStatus.FAILED
        
        contact.mark_as_sent()
        self._messages_sent += 1
        return ContactStatus.SENT
    
    def send_batch(
        self,
        contacts: List[Contact],
        template: MessageTemplate,
        progress_callback: Optional[Callable] = None,
        log_callback: Optional[Callable] = None
    ) -> dict:
        """
        Envia mensagens para multiplos contatos
        
        Args:
            contacts: Lista de contatos
            template: Template da mensagem
            progress_callback: Callback de progresso (current, total, percent)
            log_callback: Callback de log (message)
        """
        self._is_running = True
        self._should_stop = False
        
        stats = {
            "total": len(contacts),
            "sent": 0,
            "failed": 0,
            "skipped": 0,
            "invalid": 0
        }
        
        for i, contact in enumerate(contacts):
            if self._should_stop:
                if log_callback:
                    log_callback("Envio interrompido pelo usuario")
                break
            
            if log_callback:
                log_callback(f"Enviando para {contact.full_name} ({contact.phone})...")
            
            status = self.send_single(contact, template)
            
            # Atualiza estatisticas
            if status == ContactStatus.SENT:
                stats["sent"] += 1
                if log_callback:
                    log_callback(f"  [OK] Enviado para {contact.full_name}")
            elif status == ContactStatus.FAILED:
                stats["failed"] += 1
                if log_callback:
                    log_callback(f"  [ERRO] Falha: {contact.error_message}")
            elif status == ContactStatus.SKIPPED:
                stats["skipped"] += 1
                if log_callback:
                    log_callback(f"  [PULADO] Sem WhatsApp")
            elif status == ContactStatus.INVALID_PHONE:
                stats["invalid"] += 1
                if log_callback:
                    log_callback(f"  [INVALIDO] {contact.error_message}")
            
            # Callback de progresso
            if progress_callback:
                percent = ((i + 1) / len(contacts)) * 100
                progress_callback(i + 1, len(contacts), percent)
            
            # Delay entre mensagens
            if i < len(contacts) - 1 and not self._should_stop:
                self._wait_between_messages()
        
        self._is_running = False
        return stats
    
    def stop(self):
        """Para o envio"""
        self._should_stop = True
    
    def close(self):
        """Fecha o navegador"""
        if self._driver:
            self._driver.quit()
            self._driver = None
        self._is_logged_in = False
    
    @property
    def is_logged_in(self) -> bool:
        return self._is_logged_in
    
    @property
    def is_running(self) -> bool:
        return self._is_running