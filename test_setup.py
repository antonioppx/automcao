#!/usr/bin/env python3
"""
Script de teste para verificar se a instalação está funcionando
"""

import sys
import importlib
from colorama import init, Fore, Style

init()

def test_imports():
    """Testa se todas as dependências podem ser importadas"""
    print(f"{Fore.YELLOW}Testando importações...{Style.RESET_ALL}")
    
    required_modules = [
        'selenium',
        'webdriver_manager', 
        'colorama',
        'fake_useragent',
        'undetected_chromedriver'
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"{Fore.GREEN}✅ {module}{Style.RESET_ALL}")
        except ImportError as e:
            print(f"{Fore.RED}❌ {module}: {e}{Style.RESET_ALL}")
            failed_imports.append(module)
    
    return len(failed_imports) == 0

def test_local_modules():
    """Testa se os módulos locais podem ser importados"""
    print(f"\n{Fore.YELLOW}Testando módulos locais...{Style.RESET_ALL}")
    
    local_modules = [
        'instagram_automation',
        'account_manager',
        'config'
    ]
    
    failed_imports = []
    
    for module in local_modules:
        try:
            importlib.import_module(module)
            print(f"{Fore.GREEN}✅ {module}{Style.RESET_ALL}")
        except ImportError as e:
            print(f"{Fore.RED}❌ {module}: {e}{Style.RESET_ALL}")
            failed_imports.append(module)
    
    return len(failed_imports) == 0

def test_chrome_driver():
    """Testa se o ChromeDriver pode ser inicializado"""
    print(f"\n{Fore.YELLOW}Testando ChromeDriver...{Style.RESET_ALL}")
    
    try:
        import undetected_chromedriver as uc
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = uc.Chrome(options=options)
        driver.get("https://www.google.com")
        title = driver.title
        driver.quit()
        
        print(f"{Fore.GREEN}✅ ChromeDriver funcionando{Style.RESET_ALL}")
        print(f"   Página de teste carregada: {title}")
        return True
        
    except Exception as e:
        print(f"{Fore.RED}❌ ChromeDriver: {e}{Style.RESET_ALL}")
        return False

def main():
    """Função principal de teste"""
    print(f"{Fore.CYAN}=== TESTE DE CONFIGURAÇÃO ==={Style.RESET_ALL}")
    
    all_tests_passed = True
    
    # Teste 1: Importações
    if not test_imports():
        all_tests_passed = False
    
    # Teste 2: Módulos locais
    if not test_local_modules():
        all_tests_passed = False
    
    # Teste 3: ChromeDriver
    if not test_chrome_driver():
        all_tests_passed = False
    
    # Resultado final
    print(f"\n{Fore.CYAN}=== RESULTADO ==={Style.RESET_ALL}")
    
    if all_tests_passed:
        print(f"{Fore.GREEN}✅ Todos os testes passaram!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}O sistema está pronto para uso.{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}Próximo passo: Execute 'python main.py'{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}❌ Alguns testes falharam!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Execute 'python install.py' para reinstalar as dependências.{Style.RESET_ALL}")
    
    return all_tests_passed

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Teste interrompido pelo usuário.{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Fore.RED}Erro durante teste: {e}{Style.RESET_ALL}")
        sys.exit(1)
