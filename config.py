"""
Configurações do Instagram Automation
"""

class Config:
    # Configurações de delay para evitar detecção
    MIN_DELAY = 2  # segundos
    MAX_DELAY = 5  # segundos
    
    # Configurações de follow
    MAX_FOLLOWS_PER_ACCOUNT = 50  # máximo de follows por conta por sessão
    FOLLOW_DELAY_MIN = 3  # delay mínimo entre follows
    FOLLOW_DELAY_MAX = 8  # delay máximo entre follows
    
    # Configurações de navegador
    HEADLESS = False  # True para executar sem interface gráfica
    WINDOW_SIZE = (1920, 1080)
    
    # Diretórios
    ACCOUNTS_FILE = "accounts.json"
    LOGS_DIR = "logs"
    
    # Configurações de segurança
    RANDOM_USER_AGENT = True
    DISABLE_IMAGES = False  # carregar imagens normalmente
    
    @staticmethod
    def get_chrome_options():
        from selenium.webdriver.chrome.options import Options
        from fake_useragent import UserAgent
        
        options = Options()
        
        if Config.HEADLESS:
            options.add_argument("--headless")
            
        options.add_argument(f"--window-size={Config.WINDOW_SIZE[0]},{Config.WINDOW_SIZE[1]}")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        if Config.RANDOM_USER_AGENT:
            ua = UserAgent()
            options.add_argument(f"--user-agent={ua.random}")
            
        if Config.DISABLE_IMAGES:
            prefs = {"profile.managed_default_content_settings.images": 2}
            options.add_experimental_option("prefs", prefs)
            
        return options