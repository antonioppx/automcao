#!/usr/bin/env python3
"""
Script de instalação e configuração inicial
"""

import os
import sys
import subprocess
from colorama import init, Fore, Style

init()

def print_banner():
    banner = f"""
{Fore.CYAN}
╔══════════════════════════════════════════════════════════════╗
║                INSTAGRAM AUTOMATION INSTALLER               ║
║                    Instalação e Configuração                ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    print(banner)

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    print(f"{Fore.YELLOW}Verificando versão do Python...{Style.RESET_ALL}")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print(f"{Fore.RED}Erro: Python 3.7 ou superior é necessário!{Style.RESET_ALL}")
        print(f"Versão atual: {version.major}.{version.minor}.{version.micro}")
        return False
        
    print(f"{Fore.GREEN}Python {version.major}.{version.minor}.{version.micro} - OK{Style.RESET_ALL}")
    return True

def install_requirements():
    """Instala as dependências necessárias"""
    print(f"\n{Fore.YELLOW}Instalando dependências...{Style.RESET_ALL}")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print(f"{Fore.GREEN}Dependências instaladas com sucesso!{Style.RESET_ALL}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Erro ao instalar dependências: {e}{Style.RESET_ALL}")
        return False

def check_chrome():
    """Verifica se o Chrome está instalado"""
    print(f"\n{Fore.YELLOW}Verificando Google Chrome...{Style.RESET_ALL}")
    
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Users\{}\AppData\Local\Google\Chrome\Application\chrome.exe".format(os.getenv('USERNAME', ''))
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"{Fore.GREEN}Google Chrome encontrado!{Style.RESET_ALL}")
            return True
            
    print(f"{Fore.RED}Google Chrome não encontrado!{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Por favor, instale o Google Chrome antes de continuar.{Style.RESET_ALL}")
    return False

def create_sample_config():
    """Cria arquivo de configuração de exemplo"""
    print(f"\n{Fore.YELLOW}Criando arquivo de configuração de exemplo...{Style.RESET_ALL}")
    
    sample_config = {
        "accounts": [
            {
                "username": "exemplo_conta_1",
                "password": "exemplo_senha_1",
                "enabled": True,
                "last_used": None,
                "follow_count": 0,
                "status": "active"
            },
            {
                "username": "exemplo_conta_2", 
                "password": "exemplo_senha_2",
                "enabled": True,
                "last_used": None,
                "follow_count": 0,
                "status": "active"
            }
        ],
        "last_updated": "2024-01-01 12:00:00"
    }
    
    try:
        import json
        with open("accounts.json", "w", encoding="utf-8") as f:
            json.dump(sample_config, f, indent=2, ensure_ascii=False)
        print(f"{Fore.GREEN}Arquivo accounts.json criado!{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{Fore.RED}Erro ao criar arquivo de configuração: {e}{Style.RESET_ALL}")
        return False

def show_next_steps():
    """Mostra próximos passos"""
    print(f"\n{Fore.CYAN}=== INSTALAÇÃO CONCLUÍDA ==={Style.RESET_ALL}")
    print(f"{Fore.GREEN}✅ Todas as dependências foram instaladas{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✅ Arquivo de configuração criado{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}PRÓXIMOS PASSOS:{Style.RESET_ALL}")
    print("1. Edite o arquivo 'accounts.json' com suas credenciais reais")
    print("2. Execute: python main.py")
    print("3. Configure suas contas no menu")
    print("4. Execute as seguidas automáticas")
    
    print(f"\n{Fore.RED}IMPORTANTE:{Style.RESET_ALL}")
    print("- Use apenas contas válidas do Instagram")
    print("- Respeite os limites de seguidas")
    print("- Mantenha delays adequados entre ações")
    print("- Monitore os logs regularmente")

def main():
    """Função principal de instalação"""
    print_banner()
    
    print(f"{Fore.YELLOW}Iniciando instalação do Instagram Automation...{Style.RESET_ALL}")
    
    # Verificações
    if not check_python_version():
        return False
        
    if not check_chrome():
        return False
        
    # Instalação
    if not install_requirements():
        return False
        
    if not create_sample_config():
        return False
        
    # Próximos passos
    show_next_steps()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print(f"\n{Fore.GREEN}Instalação concluída com sucesso!{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}Instalação falhou!{Style.RESET_ALL}")
            sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Instalação interrompida pelo usuário.{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Fore.RED}Erro inesperado durante instalação: {e}{Style.RESET_ALL}")
        sys.exit(1)
