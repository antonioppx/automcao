#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
from account_manager import AccountManager
from config import Config

def print_banner():
    """Exibe o banner do programa"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    INSTAGRAM FOLLOW BOT                      ║
    ║                                                              ║
    ║  Automação para seguir usuários com múltiplas contas        ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def create_sample_accounts():
    """Cria arquivo de exemplo com contas"""
    sample_accounts = [
        {
            "username": "sua_conta_1",
            "password": "sua_senha_1",
            "account_id": "conta_1",
            "active": True,
            "last_used": None,
            "follows_today": 0
        },
        {
            "username": "sua_conta_2", 
            "password": "sua_senha_2",
            "account_id": "conta_2",
            "active": True,
            "last_used": None,
            "follows_today": 0
        }
    ]
    
    with open("accounts.json", "w", encoding="utf-8") as f:
        json.dump(sample_accounts, f, indent=2, ensure_ascii=False)
    
    print("✅ Arquivo accounts.json criado com exemplos!")
    print("📝 Edite o arquivo com suas contas reais antes de usar.")

def menu_principal():
    """Menu principal do programa"""
    manager = AccountManager()
    
    while True:
        print("\n" + "="*60)
        print("MENU PRINCIPAL")
        print("="*60)
        print("1. Gerenciar contas")
        print("2. Executar follow automático")
        print("3. Configurações")
        print("4. Ver estatísticas")
        print("5. Sair")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            menu_contas(manager)
        elif opcao == "2":
            menu_follow(manager)
        elif opcao == "3":
            menu_configuracoes()
        elif opcao == "4":
            ver_estatisticas(manager)
        elif opcao == "5":
            print("👋 Até logo!")
            break
        else:
            print("❌ Opção inválida!")

def menu_contas(manager):
    """Menu de gerenciamento de contas"""
    while True:
        print("\n" + "-"*40)
        print("GERENCIAR CONTAS")
        print("-"*40)
        print("1. Adicionar conta")
        print("2. Remover conta")
        print("3. Listar contas")
        print("4. Voltar")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            adicionar_conta(manager)
        elif opcao == "2":
            remover_conta(manager)
        elif opcao == "3":
            listar_contas(manager)
        elif opcao == "4":
            break
        else:
            print("❌ Opção inválida!")

def adicionar_conta(manager):
    """Adiciona uma nova conta"""
    print("\n--- ADICIONAR CONTA ---")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    account_id = input("ID da conta (opcional): ").strip() or username
    
    if username and password:
        manager.add_account(username, password, account_id)
    else:
        print("❌ Username e password são obrigatórios!")

def remover_conta(manager):
    """Remove uma conta"""
    print("\n--- REMOVER CONTA ---")
    if not manager.accounts:
        print("❌ Nenhuma conta cadastrada!")
        return
        
    listar_contas(manager)
    username = input("\nUsername da conta a remover: ").strip()
    
    if username:
        manager.remove_account(username)

def listar_contas(manager):
    """Lista todas as contas"""
    print("\n--- CONTAS CADASTRADAS ---")
    if not manager.accounts:
        print("❌ Nenhuma conta cadastrada!")
        return
        
    for i, account in enumerate(manager.accounts, 1):
        status = "✅ Ativa" if account.get("active", True) else "❌ Inativa"
        follows = account.get("follows_today", 0)
        last_used = account.get("last_used", "Nunca")
        
        print(f"{i}. {account['username']} ({account['account_id']})")
        print(f"   Status: {status}")
        print(f"   Follows hoje: {follows}")
        print(f"   Último uso: {last_used}")
        print()

def menu_follow(manager):
    """Menu de execução de follow"""
    print("\n--- FOLLOW AUTOMÁTICO ---")
    
    if not manager.get_active_accounts():
        print("❌ Nenhuma conta ativa encontrada!")
        print("💡 Adicione contas no menu 'Gerenciar contas' primeiro.")
        return
    
    # Lista de usuários para seguir
    print("Digite os usernames dos usuários que deseja seguir (separados por vírgula):")
    usernames_input = input("Usernames: ").strip()
    
    if not usernames_input:
        print("❌ Nenhum username informado!")
        return
        
    target_usernames = [u.strip() for u in usernames_input.split(",") if u.strip()]
    
    if not target_usernames:
        print("❌ Nenhum username válido!")
        return
    
    print(f"\n🎯 Alvos: {', '.join(target_usernames)}")
    print(f"📊 Contas ativas: {len(manager.get_active_accounts())}")
    
    # Modo de execução
    print("\nEscolha o modo de execução:")
    print("1. Sequencial (uma conta por vez - mais seguro)")
    print("2. Paralelo (todas as contas simultaneamente - mais rápido)")
    
    modo = input("Modo (1 ou 2): ").strip()
    
    # Limite de contas
    max_accounts = input("Máximo de contas a usar (Enter para todas): ").strip()
    max_accounts = int(max_accounts) if max_accounts.isdigit() else None
    
    # Confirmação
    print(f"\n⚠️  CONFIRMAÇÃO:")
    print(f"   Alvos: {', '.join(target_usernames)}")
    print(f"   Modo: {'Sequencial' if modo == '1' else 'Paralelo'}")
    print(f"   Contas: {max_accounts or 'Todas'}")
    
    confirmar = input("\nContinuar? (s/N): ").strip().lower()
    
    if confirmar in ['s', 'sim', 'y', 'yes']:
        print("\n🚀 Iniciando follow automático...")
        
        if modo == "1":
            manager.follow_users_sequential(target_usernames, max_accounts)
        else:
            manager.follow_users_parallel(target_usernames, max_accounts)
    else:
        print("❌ Operação cancelada!")

def menu_configuracoes():
    """Menu de configurações"""
    print("\n--- CONFIGURAÇÕES ---")
    print("1. Configurações de delay")
    print("2. Configurações de follow")
    print("3. Configurações do navegador")
    print("4. Voltar")
    
    opcao = input("\nEscolha uma opção: ").strip()
    
    if opcao == "1":
        print(f"Delay mínimo: {Config.MIN_DELAY}s")
        print(f"Delay máximo: {Config.MAX_DELAY}s")
        print("💡 Edite o arquivo config.py para alterar")
    elif opcao == "2":
        print(f"Máximo de follows por conta: {Config.MAX_FOLLOWS_PER_ACCOUNT}")
        print(f"Delay entre follows: {Config.FOLLOW_DELAY_MIN}-{Config.FOLLOW_DELAY_MAX}s")
        print("💡 Edite o arquivo config.py para alterar")
    elif opcao == "3":
        print(f"Modo headless: {Config.HEADLESS}")
        print(f"Tamanho da janela: {Config.WINDOW_SIZE}")
        print("💡 Edite o arquivo config.py para alterar")

def ver_estatisticas(manager):
    """Exibe estatísticas das contas"""
    print("\n--- ESTATÍSTICAS ---")
    
    if not manager.accounts:
        print("❌ Nenhuma conta cadastrada!")
        return
    
    total_follows = sum(acc.get("follows_today", 0) for acc in manager.accounts)
    contas_ativas = len(manager.get_active_accounts())
    
    print(f"📊 Total de contas: {len(manager.accounts)}")
    print(f"✅ Contas ativas: {contas_ativas}")
    print(f"📈 Total de follows hoje: {total_follows}")
    
    print("\n📋 Detalhes por conta:")
    for account in manager.accounts:
        status = "✅" if account.get("active", True) else "❌"
        follows = account.get("follows_today", 0)
        print(f"   {status} {account['username']}: {follows} follows")

def main():
    """Função principal"""
    print_banner()
    
    # Verifica se o arquivo de contas existe
    if not os.path.exists("accounts.json"):
        print("📁 Arquivo accounts.json não encontrado!")
        criar = input("Criar arquivo de exemplo? (s/N): ").strip().lower()
        
        if criar in ['s', 'sim', 'y', 'yes']:
            create_sample_accounts()
        else:
            print("❌ É necessário ter contas cadastradas para usar o programa!")
            return
    
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrompido pelo usuário!")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {str(e)}")

if __name__ == "__main__":
    main()