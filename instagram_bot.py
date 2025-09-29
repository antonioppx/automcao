import time
import random
import json
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import undetected_chromedriver as uc
from config import Config
import logging

class InstagramBot:
    def __init__(self, username, password, account_id=None):
        self.username = username
        self.password = password
        self.account_id = account_id or username
        self.driver = None
        self.logger = self._setup_logger()
        self.followed_count = 0
        
    def _setup_logger(self):
        """Configura o sistema de logs para cada conta"""
        if not os.path.exists(Config.LOGS_DIR):
            os.makedirs(Config.LOGS_DIR)
            
        logger = logging.getLogger(f"instagram_bot_{self.account_id}")
        logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler(f"{Config.LOGS_DIR}/{self.account_id}_{datetime.now().strftime('%Y%m%d')}.log")
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
        
    def _random_delay(self, min_delay=None, max_delay=None):
        """Aplica delay aleatório para evitar detecção"""
        min_delay = min_delay or Config.MIN_DELAY
        max_delay = max_delay or Config.MAX_DELAY
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
        
    def _human_like_typing(self, element, text):
        """Simula digitação humana"""
        element.clear()
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
            
    def start_browser(self):
        """Inicia o navegador com configurações otimizadas"""
        try:
            self.driver = uc.Chrome(options=Config.get_chrome_options())
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.logger.info(f"Navegador iniciado para conta {self.account_id}")
            return True
        except Exception as e:
            self.logger.error(f"Erro ao iniciar navegador: {str(e)}")
            return False
            
    def login(self):
        """Faz login na conta do Instagram"""
        try:
            self.driver.get("https://www.instagram.com/accounts/login/")
            self._random_delay(3, 5)
            
            # Aguarda os campos de login aparecerem
            wait = WebDriverWait(self.driver, 10)
            username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
            password_field = self.driver.find_element(By.NAME, "password")
            
            # Digita as credenciais
            self._human_like_typing(username_field, self.username)
            self._random_delay(1, 2)
            self._human_like_typing(password_field, self.password)
            self._random_delay(1, 2)
            
            # Clica no botão de login
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # Aguarda o login ser processado
            self._random_delay(5, 8)
            
            # Verifica se o login foi bem-sucedido
            if "instagram.com" in self.driver.current_url and "login" not in self.driver.current_url:
                self.logger.info(f"Login realizado com sucesso para {self.account_id}")
                return True
            else:
                self.logger.error(f"Falha no login para {self.account_id}")
                return False
                
        except Exception as e:
            self.logger.error(f"Erro durante login: {str(e)}")
            return False
            
    def follow_user(self, target_username):
        """Segue um usuário específico"""
        try:
            # Navega para o perfil do usuário
            profile_url = f"https://www.instagram.com/{target_username}/"
            self.driver.get(profile_url)
            self._random_delay(3, 5)
            
            # Verifica se o perfil existe
            if "Page Not Found" in self.driver.page_source or "Sorry, this page isn't available" in self.driver.page_source:
                self.logger.warning(f"Perfil {target_username} não encontrado")
                return False
                
            # Procura pelo botão de seguir
            wait = WebDriverWait(self.driver, 10)
            follow_button = None
            
            # Tenta diferentes seletores para o botão de seguir
            selectors = [
                "//button[contains(text(), 'Follow')]",
                "//button[contains(text(), 'Seguir')]",
                "//button[contains(@class, '_acan') and contains(text(), 'Follow')]",
                "//button[contains(@class, '_acan') and contains(text(), 'Seguir')]"
            ]
            
            for selector in selectors:
                try:
                    follow_button = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    break
                except TimeoutException:
                    continue
                    
            if not follow_button:
                # Verifica se já está seguindo
                if "Following" in self.driver.page_source or "Seguindo" in self.driver.page_source:
                    self.logger.info(f"Já está seguindo {target_username}")
                    return True
                else:
                    self.logger.warning(f"Botão de seguir não encontrado para {target_username}")
                    return False
                    
            # Clica no botão de seguir
            self.driver.execute_script("arguments[0].click();", follow_button)
            self._random_delay(Config.FOLLOW_DELAY_MIN, Config.FOLLOW_DELAY_MAX)
            
            self.followed_count += 1
            self.logger.info(f"Seguiu {target_username} com sucesso (total: {self.followed_count})")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao seguir {target_username}: {str(e)}")
            return False
            
    def follow_multiple_users(self, usernames):
        """Segue múltiplos usuários"""
        successful_follows = 0
        failed_follows = 0
        
        for username in usernames:
            if self.followed_count >= Config.MAX_FOLLOWS_PER_ACCOUNT:
                self.logger.info(f"Limite de follows atingido para {self.account_id}")
                break
                
            if self.follow_user(username):
                successful_follows += 1
            else:
                failed_follows += 1
                
            # Delay entre follows
            self._random_delay(Config.FOLLOW_DELAY_MIN, Config.FOLLOW_DELAY_MAX)
            
        self.logger.info(f"Resultado: {successful_follows} sucessos, {failed_follows} falhas")
        return successful_follows, failed_follows
        
    def close(self):
        """Fecha o navegador"""
        if self.driver:
            self.driver.quit()
            self.logger.info(f"Navegador fechado para {self.account_id}")
