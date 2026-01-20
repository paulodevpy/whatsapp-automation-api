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
        self._clean_profile_on_init = True  # Limpar cache na primeira inicialização
    
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
    
    def _clean_chrome_profile(self):
        """Limpa o perfil do Chrome para remover cache corrompido"""
        profile_path = Path(config.CHROME_PROFILE_DIR)
        
        if not profile_path.exists():
            print(f"Criando novo perfil do Chrome em: {profile_path}")
            profile_path.mkdir(parents=True, exist_ok=True)
            return
        
        print("Limpando cache do perfil do Chrome...")
        
        # Pastas que causam problemas (cache, dados de site, etc)
        folders_to_clean = [
            "Cache",
            "Code Cache",
            "Cookies",
            "Session Storage",
            "Service Worker",
            "FileSystem",
            "databases",
            "Local Storage",
            "Default/Service Worker"
        ]
        
        default_path = profile_path / "Default"
        if default_path.exists():
            for folder in folders_to_clean:
                folder_path = default_path / folder
                if folder_path.exists():
                    try:
                        shutil.rmtree(folder_path)
                        print(f"  - Removido: {folder}")
                    except Exception as e:
                        print(f"  - Erro ao remover {folder}: {e}")
        
        print("Perfil limpo!")
    
    def initialize(self) -> bool:
        """Inicializa o driver do navegador"""
        try:
            import tempfile
            
            options = Options()
            
            # Argumentos mínimos - remover argumentos que causam crash
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Argumentos essenciais apenas
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')
            options.add_argument('--start-maximized')
            options.add_argument('--disable-notifications')
            
            # Usa perfil persistente do Chrome
            options.add_argument(f'--user-data-dir={config.CHROME_PROFILE_DIR}')
            
            # Garante que o ChromeDriver esteja disponivel
            driver_exe = self._ensure_chromedriver()
            service = Service(driver_exe)
            
            print("Iniciando Chrome...")
            self._driver = webdriver.Chrome(service=service, options=options)
            
            # Define timeout
            self._driver.set_page_load_timeout(30)
            self._driver.implicitly_wait(1)
            
            # Remove flag webdriver
            self._driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )
            
            print("✓ Chrome iniciado!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao inicializar Chrome: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def login(self, timeout: int = 300) -> bool:
        """
        Abre WhatsApp Web e aguarda login + carregamento das conversas
        
        Args:
            timeout: Tempo maximo de espera em segundos (padrão: 5 minutos)
        """
        if not self._driver:
            print("Driver não inicializado!")
            return False
        
        try:
            print("=" * 60)
            print("Abrindo https://web.whatsapp.com...")
            print("=" * 60)
            self._driver.get("https://web.whatsapp.com")
            
            start_time = time.time()
            
            # Fase 1: Aguarda página carregar (QR code ou já logado)
            print("\n[FASE 1] Aguardando carregamento da página...")
            try:
                WebDriverWait(self._driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="app"]'))
                )
                print("✓ Página carregada!")
            except TimeoutException:
                print("⚠️  Página não carregou, tentando com canvas...")
            
            # Fase 2: Aguarda QR code ou elementos de login
            print("\n[FASE 2] Detectando status de login...")
            
            # Tenta detectar QR code
            qr_code_detected = False
            try:
                canvas = WebDriverWait(self._driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//canvas'))
                )
                qr_code_detected = canvas.is_displayed()
                print("✓ Canvas detectado (QR code)")
            except TimeoutException:
                print("ℹ️  Nenhum QR code visível - pode já estar logado")
            
            if qr_code_detected:
                print("\n" + "=" * 60)
                print("⚠️  QR CODE DETECTADO!")
                print("=" * 60)
                print("Por favor, escaneie o QR code com seu celular.")
                print(f"Tempo disponível: {timeout}s")
                print("=" * 60)
                
                # Fase 3: Aguarda scan do QR code
                print("\n[FASE 3] Aguardando que você escaneie o QR code...")
                print("Esperando elementos da interface de chat aparecerem...")
                
                try:
                    # Aguarda um desses elementos aparecer (significa que foi logado)
                    WebDriverWait(self._driver, timeout).until(
                        lambda driver: (
                            self._element_clickable(driver, '//div[@contenteditable="true"][@data-tab="3"]') or
                            self._element_clickable(driver, '//div[contains(@aria-label, "Type a message")]') or
                            self._element_clickable(driver, '//*[@id="main"]//footer//div[@contenteditable="true"]') or
                            len(driver.find_elements(By.XPATH, '//*[@id="pane-side"]//div[contains(@class, "chat")]')) > 0
                        )
                    )
                    print("\n✓ QR code escaneado com sucesso!")
                    print("✓ Login realizado!")
                    
                except TimeoutException:
                    print(f"\n❌ Timeout: QR code não foi escaneado em {timeout}s")
                    return False
            else:
                print("\n[FASE 3] Já logado - aguardando carregamento da interface...")
            
            # Fase 4: Aguarda carregamento completo das conversas
            print("\n[FASE 4] Aguardando carregamento das conversas...")
            
            try:
                # Aguarda que a lista de conversas carregue
                WebDriverWait(self._driver, 60).until(
                    lambda driver: (
                        len(driver.find_elements(By.XPATH, '//*[@id="pane-side"]//div[contains(@class, "chat")]')) > 0 or
                        driver.find_element(By.XPATH, '//*[@id="pane-side"]//div[@role="list"]').is_displayed()
                    )
                )
                print("✓ Conversas carregadas!")
                
            except TimeoutException:
                print("⚠️  Timeout ao aguardar conversas (pode estar demorando mais)")
            except:
                pass
            
            # Fase 5: Aguarda elementos de interação
            print("\n[FASE 5] Aguardando elementos de interação...")
            
            try:
                WebDriverWait(self._driver, 30).until(
                    EC.presence_of_element_located((
                        By.XPATH, 
                        '//div[@contenteditable="true"][@data-tab="3"] | //div[contains(@aria-label, "Type a message")] | //*[@id="main"]//footer//div[@contenteditable="true"]'
                    ))
                )
                print("✓ Caixa de mensagem disponível!")
                
            except TimeoutException:
                print("⚠️  Timeout ao aguardar caixa de mensagem")
            
            # Aguarda um pouco para interface stabilizar
            print("\n[FASE 6] Estabilizando interface...")
            time.sleep(2)
            
            print("\n" + "=" * 60)
            print("✓✓✓ WhatsApp Web está PRONTO! ✓✓✓")
            print("=" * 60 + "\n")
            
            self._is_logged_in = True
            return True
            
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"\n❌ ERRO: {e}")
            print(f"Tempo decorrido: {elapsed:.0f}s / {timeout}s")
            print(f"URL atual: {self._driver.current_url}")
            import traceback
            traceback.print_exc()
            return False
    
    def _element_exists(self, driver, xpath: str) -> bool:
        """Verifica se um elemento existe na página"""
        try:
            driver.find_element(By.XPATH, xpath)
            return True
        except:
            return False
    
    def _element_visible(self, driver, xpath: str) -> bool:
        """Verifica se um elemento está visível na página"""
        try:
            elem = driver.find_element(By.XPATH, xpath)
            return elem.is_displayed()
        except:
            return False
    
    def _element_clickable(self, driver, xpath: str) -> bool:
        """Verifica se um elemento está visível e clicável"""
        try:
            elem = driver.find_element(By.XPATH, xpath)
            return elem.is_displayed() and elem.is_enabled()
        except:
            return False
    
    def _check_number_exists(self) -> bool:
        """Verifica se numero tem WhatsApp"""
        print("  Verificando contato...")
        
        try:
            # Verifica caixa de mensagem primeiro (máximo 5s)
            message_box_xpaths = [
                '//div[@contenteditable="true"][@data-tab="3"]',
                '//div[contains(@aria-label, "Type a message")]',
                '//*[@id="main"]//footer//div[@contenteditable="true"]',
            ]
            
            for msg_xpath in message_box_xpaths:
                try:
                    WebDriverWait(self._driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, msg_xpath))
                    )
                    print("  ✓ Contato ok")
                    return True
                except:
                    pass
            
            # Se falhou, verifica erros
            error_xpaths = [
                "//span[contains(text(), 'This contact does not have WhatsApp')]",
                "//span[@data-testid='error']",
            ]
            
            for error_xpath in error_xpaths:
                try:
                    elem = self._driver.find_element(By.XPATH, error_xpath)
                    if elem.is_displayed():
                        print("  ❌ Sem WhatsApp")
                        return False
                except:
                    pass
            
            print("  ⚠️  Verificação indefinida")
            return False
                
        except Exception as e:
            print(f"  ⚠️  Erro: {str(e)[:40]}")
            return False
    
    def _open_chat(self, phone: str) -> bool:
        """Abre conversa com numero"""
        print(f"  Abrindo: {phone}")
        self._driver.get(f"https://web.whatsapp.com/send?phone={phone}")
        return self._check_number_exists()
    
    def _send_text(self, message: str) -> bool:
        """Envia mensagem de texto"""
        try:
            # XPath específico para a caixa de mensagem
            message_box_xpath = '//*[@id="main"]/footer/div[1]/div/span/div/div/div/div[3]/div[1]/p'
            
            msg_box = WebDriverWait(self._driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, message_box_xpath))
            )
            
            # Clica e envia
            msg_box.click()
            
            # Envia em blocos rápidos
            lines = message.split('\n')
            for i, line in enumerate(lines):
                chunk_size = random.randint(20, 35)
                for j in range(0, len(line), chunk_size):
                    msg_box.send_keys(line[j:j + chunk_size])
                    time.sleep(random.uniform(0.01, 0.02))
                
                if i < len(lines) - 1:
                    msg_box.send_keys(Keys.SHIFT + Keys.ENTER)
            
            msg_box.send_keys(Keys.ENTER)
            print(f"  ✓ Enviada ({len(message)} chars)")
            return True
            
        except Exception as e:
            print(f"  ❌ Erro: {str(e)[:40]}")
            return False
    
    def _send_image(self, image_path: str) -> bool:
        """Envia imagem"""
        print(f"  Enviando imagem...")
        try:
            # XPath para o botão de anexo
            attach_xpath = '//*[@id="main"]/footer/div[1]/div/span/div/div/div/div[1]/div/span/button/div/div/div[1]/span'
            
            attach_btn = WebDriverWait(self._driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, attach_xpath))
            )
            attach_btn.click()
            
            # Clica em Fotos e vídeos
            photos_xpath = '//*[@id="app"]/div/div/div[4]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[2]/div[1]/div[2]/span'
            
            photos_btn = WebDriverWait(self._driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, photos_xpath))
            )
            photos_btn.click()
            
            # Campo de arquivo
            try:
                img_input = WebDriverWait(self._driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
                )
                img_input.send_keys(str(Path(image_path).resolve()))
                print("  ✓ Arquivo selecionado")
            except:
                print("  ❌ Campo de arquivo não encontrado")
                return False
            
            # Clica no botão de envio
            time.sleep(0.5)
            send_btn_xpath = '//*[@id="app"]/div/div/div[3]/div/div[3]/div[2]/div/span/div/div/div/div[2]/div/div[2]/div[2]/span/div/div/span'
            
            send_btn = WebDriverWait(self._driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, send_btn_xpath))
            )
            send_btn.click()
            
            print("  ✓ Imagem enviada")
            return True
            
        except Exception as e:
            print(f"  ❌ Erro: {str(e)[:40]}")
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
            print(f"  ⏸️  Pausa {config.PAUSE_DURATION}s")
            self._take_pause()
        
        # Abre chat
        if not self._open_chat(contact.phone):
            contact.mark_as_skipped()
            return ContactStatus.SKIPPED
        
        # Envia texto
        message = template.render(contact)
        if not self._send_text(message):
            contact.mark_as_failed("Falha ao enviar texto")
            return ContactStatus.FAILED
        
        # Envia imagem
        if template.has_image():
            if not self._send_image(template.image_path):
                contact.mark_as_failed("Falha ao enviar imagem")
                return ContactStatus.FAILED
        
        contact.mark_as_sent()
        self._messages_sent += 1
        
        # Aguarda entre mensagens
        self._wait_between_messages()
        
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
        try:
            if self._driver:
                self._driver.quit()
                self._driver = None
            self._is_logged_in = False
        except Exception as e:
            print(f"Erro ao fechar driver: {e}")
            self._driver = None
            self._is_logged_in = False
    
    @property
    def is_logged_in(self) -> bool:
        return self._is_logged_in
    
    @property
    def is_running(self) -> bool:
        return self._is_running