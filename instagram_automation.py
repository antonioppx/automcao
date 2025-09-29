import time
import random
import json
import logging
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import undetected_chromedriver as uc
from fake_useragent import UserAgent
from colorama import init, Fore, Style

# Inicializar colorama para cores no terminal
init()

class InstagramAutomation:
    def __init__(self, headless: bool = False, debug: bool = False):
        """
        Inicializa a automação do Instagram
        
        Args:
            headless: Se True, executa o navegador em modo headless
            debug: Se True, ativa logs detalhados
        """
        self.headless = headless
        self.debug = debug
        self.driver = None
        self.wait = None
        self.logged_in = False
        
        # Configurar logging
        self.setup_logging()
        
        # Configurar user agent
        self.ua = UserAgent()
        
    def setup_logging(self):
        """Configura o sistema de logging"""
        level = logging.DEBUG if self.debug else logging.INFO
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('instagram_automation.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_driver(self):
        """Configura e inicializa o driver do Chrome"""
        try:
            self.logger.info("Configurando driver do Chrome...")
            
            # Configurações do Chrome
            options = uc.ChromeOptions()
            
            if self.headless:
                # Em versões recentes do Chrome, use o modo headless "new"
                options.add_argument('--headless=new')
            
            # Configurações para melhorar estabilidade
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-infobars')
            options.add_argument('--disable-blink-features=AutomationControlled')
            
            # User agent aleatório
            user_agent = self.ua.random
            options.add_argument(f'--user-agent={user_agent}')
            
            # Inicializar driver
            self.driver = uc.Chrome(options=options, use_subprocess=True)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # Configurar timeout
            self.wait = WebDriverWait(self.driver, 20)
            
            self.logger.info("Driver configurado com sucesso!")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao configurar driver: {str(e)}")
            return False
            
    def login(self, username: str, password: str) -> bool:
        """
        Faz login no Instagram
        
        Args:
            username: Nome de usuário
            password: Senha
            
        Returns:
            True se login bem-sucedido, False caso contrário
        """
        try:
            self.logger.info(f"Tentando fazer login com usuário: {username}")
            
            # Ir para página de login
            self.driver.get("https://www.instagram.com/accounts/login/")
            self.random_delay(2, 4)
            
            # Aguardar campos de login aparecerem
            username_field = self.wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            password_field = self.driver.find_element(By.NAME, "password")
            
            # Preencher campos com delay humano
            self.human_type(username_field, username)
            self.random_delay(1, 2)
            self.human_type(password_field, password)
            self.random_delay(1, 2)
            
            # Clicar no botão de login
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # Aguardar redirecionamento ou erro
            self.random_delay(3, 5)
            
            # Verificar se login foi bem-sucedido
            if "challenge" in self.driver.current_url or "two_factor" in self.driver.current_url:
                self.logger.warning("Verificação de segurança detectada. Login pode ter falhado.")
                return False
                
            # Verificar se estamos na página principal
            try:
                self.wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/direct/inbox/')]")))
                self.logged_in = True
                self.logger.info(f"Login realizado com sucesso para {username}")
                return True
            except TimeoutException:
                self.logger.error("Login falhou - não foi possível acessar a página principal")
                return False
                
        except Exception as e:
            self.logger.error(f"Erro durante login: {str(e)}")
            return False
            
    def follow_user(self, username: str) -> bool:
        """
        Segue um usuário específico
        
        Args:
            username: Nome do usuário a ser seguido
            
        Returns:
            True se seguiu com sucesso, False caso contrário
        """
        try:
            if not self.logged_in:
                self.logger.error("Não está logado. Faça login primeiro.")
                return False
                
            self.logger.info(f"Tentando seguir usuário: {username}")
            
            # Ir para o perfil do usuário
            profile_url = f"https://www.instagram.com/{username}/"
            self.driver.get(profile_url)
            self.random_delay(2, 4)
            
            # Verificar se o perfil existe
            try:
                self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "main")))
            except TimeoutException:
                self.logger.error(f"Perfil {username} não encontrado ou inacessível")
                return False
                
            # Tentar fechar diálogos que possam cobrir o botão (cookies, salvar login, notificações)
            try:
                dismiss_selectors = [
                    "//button[contains(., 'Agora não')]",
                    "//div[@role='dialog']//button[contains(., 'Agora não')]",
                    "//button[contains(., 'Not now')]",
                ]
                for sel in dismiss_selectors:
                    els = self.driver.find_elements(By.XPATH, sel)
                    if els:
                        self.driver.execute_script("arguments[0].click();", els[0])
                        self.random_delay(0.5, 1.2)
            except Exception:
                pass

            # Procurar botão de seguir (múltiplas variações/línguas)
            selectors = [
                "//button[normalize-space()='Seguir']",
                "//button[normalize-space()='Follow']",
                "//div[@role='button' and (normalize-space()='Seguir' or normalize-space()='Follow')]",
                "//button[contains(@class,'_acan') and contains(@class,'_acap') and not(contains(., 'Following')) and not(contains(., 'Seguindo'))]",
                "//*[@aria-label='Follow' or @aria-label='Seguir']",
            ]

            follow_button = None
            for sel in selectors:
                try:
                    follow_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, sel)))
                    if follow_button:
                        break
                except TimeoutException:
                    continue

            if follow_button is None:
                # Verificar se já está seguindo
                already_selectors = [
                    "//button[normalize-space()='Seguindo']",
                    "//button[normalize-space()='Following']",
                    "//div[@role='button' and (normalize-space()='Seguindo' or normalize-space()='Following')]",
                ]
                for sel in already_selectors:
                    if self.driver.find_elements(By.XPATH, sel):
                        self.logger.info(f"Já está seguindo {username}")
                        return True

                self.logger.error(f"Botão de seguir não encontrado para {username}")
                return False

            # Clicar no botão de seguir (via JS para evitar overlay)
            self.driver.execute_script("arguments[0].click();", follow_button)
            
            self.random_delay(1, 3)
            self.logger.info(f"Seguiu com sucesso: {username}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao seguir {username}: {str(e)}")
            return False
            
    def follow_multiple_users(self, usernames: List[str], delay_range: tuple = (3, 8)) -> Dict[str, bool]:
        """
        Segue múltiplos usuários
        
        Args:
            usernames: Lista de nomes de usuários
            delay_range: Tupla com delay mínimo e máximo entre seguidas
            
        Returns:
            Dicionário com resultado para cada usuário
        """
        results = {}
        
        for i, username in enumerate(usernames):
            self.logger.info(f"Processando usuário {i+1}/{len(usernames)}: {username}")
            
            success = self.follow_user(username)
            results[username] = success
            
            # Delay entre seguidas (exceto na última)
            if i < len(usernames) - 1:
                delay = random.uniform(delay_range[0], delay_range[1])
                self.logger.info(f"Aguardando {delay:.1f} segundos antes da próxima...")
                time.sleep(delay)
                
        return results
        
    def human_type(self, element, text: str):
        """Simula digitação humana"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
            
    def random_delay(self, min_seconds: float, max_seconds: float):
        """Aplica delay aleatório"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
        
    def close(self):
        """Fecha o driver"""
        if self.driver:
            self.driver.quit()
            self.logger.info("Driver fechado")
            
    def __enter__(self):
        """Context manager entry"""
        if self.setup_driver():
            return self
        else:
            raise Exception("Falha ao configurar driver")
            
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
