import json
import time
import random
from typing import List, Dict, Optional
from instagram_automation import InstagramAutomation
import logging
from colorama import Fore, Style

class AccountManager:
    def __init__(self, config_file: str = "accounts.json"):
        """
        Gerencia múltiplas contas do Instagram
        
        Args:
            config_file: Caminho para arquivo de configuração das contas
        """
        self.config_file = config_file
        self.accounts = []
        self.logger = logging.getLogger(__name__)
        
    def load_accounts(self) -> bool:
        """
        Carrega contas do arquivo de configuração
        
        Returns:
            True se carregou com sucesso, False caso contrário
        """
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                raw_accounts = data.get('accounts', [])
                # normalizar enabled/account_id
                self.accounts = []
                for acc in raw_accounts:
                    normalized = dict(acc)
                    normalized['account_id'] = acc.get('account_id') or acc.get('username')
                    enabled_val = acc.get('enabled', True)
                    if enabled_val in ["", None]:
                        enabled_val = True
                    normalized['enabled'] = True if enabled_val in [True, 'true', 'True', 1, '1'] else bool(enabled_val)
                    self.accounts.append(normalized)
                
            self.logger.info(f"Carregadas {len(self.accounts)} contas")
            return True
            
        except FileNotFoundError:
            self.logger.error(f"Arquivo {self.config_file} não encontrado")
            return False
        except json.JSONDecodeError as e:
            self.logger.error(f"Erro ao decodificar JSON: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"Erro ao carregar contas: {str(e)}")
            return False
            
    def save_accounts(self) -> bool:
        """
        Salva contas no arquivo de configuração
        
        Returns:
            True se salvou com sucesso, False caso contrário
        """
        try:
            data = {
                'accounts': self.accounts,
                'last_updated': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            self.logger.info("Contas salvas com sucesso")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao salvar contas: {str(e)}")
            return False
            
    def add_account(self, username: str, password: str, account_id: Optional[str] = None, enabled: bool = True) -> bool:
        """
        Adiciona uma nova conta
        
        Args:
            username: Nome de usuário
            password: Senha
            enabled: Se a conta está ativa
            
        Returns:
            True se adicionou com sucesso, False caso contrário
        """
        # Verificar se conta já existe
        for account in self.accounts:
            if account['username'] == username:
                self.logger.warning(f"Conta {username} já existe")
                return False
                
        new_account = {
            'username': username,
            'password': password,
            'account_id': account_id or username,
            'enabled': True if enabled in [True, 'true', 'True', 1, '1'] else bool(enabled),
            'last_used': None,
            'follow_count': 0,
            'status': 'active'
        }
        
        self.accounts.append(new_account)
        self.logger.info(f"Conta {username} adicionada")
        return True
        
    def remove_account(self, username: str) -> bool:
        """
        Remove uma conta
        
        Args:
            username: Nome de usuário da conta a ser removida
            
        Returns:
            True se removeu com sucesso, False caso contrário
        """
        for i, account in enumerate(self.accounts):
            if account['username'] == username:
                del self.accounts[i]
                self.logger.info(f"Conta {username} removida")
                return True
                
        self.logger.warning(f"Conta {username} não encontrada")
        return False
        
    def get_active_accounts(self) -> List[Dict]:
        """
        Retorna lista de contas ativas
        
        Returns:
            Lista de contas ativas
        """
        return [account for account in self.accounts if account.get('enabled', True)]
        
    def update_account_status(self, username: str, status: str, follow_count: int = None):
        """
        Atualiza status de uma conta
        
        Args:
            username: Nome de usuário
            status: Novo status ('active', 'blocked', 'error')
            follow_count: Número de seguidas realizadas
        """
        for account in self.accounts:
            if account['username'] == username:
                account['status'] = status
                account['last_used'] = time.strftime('%Y-%m-%d %H:%M:%S')
                if follow_count is not None:
                    account['follow_count'] = follow_count
                break
                
    def follow_with_multiple_accounts(self, target_usernames: List[str], 
                                    max_follows_per_account: int = 10,
                                    delay_between_accounts: tuple = (30, 60)) -> Dict:
        """
        Usa múltiplas contas para seguir usuários alvo
        
        Args:
            target_usernames: Lista de usuários a serem seguidos
            max_follows_per_account: Máximo de seguidas por conta
            delay_between_accounts: Delay entre troca de contas
            
        Returns:
            Dicionário com resultados detalhados
        """
        active_accounts = self.get_active_accounts()
        
        if not active_accounts:
            self.logger.error("Nenhuma conta ativa encontrada")
            return {'success': False, 'error': 'Nenhuma conta ativa'}
            
        if not target_usernames:
            self.logger.error("Nenhum usuário alvo especificado")
            return {'success': False, 'error': 'Nenhum usuário alvo'}
            
        results = {
            'success': True,
            'total_targets': len(target_usernames),
            'accounts_used': 0,
            'total_follows': 0,
            'account_results': {}
        }
        
        # Dividir usuários entre as contas
        users_per_account = len(target_usernames) // len(active_accounts)
        remaining_users = len(target_usernames) % len(active_accounts)
        
        user_index = 0
        
        for i, account in enumerate(active_accounts):
            if user_index >= len(target_usernames):
                break
                
            # Calcular quantos usuários esta conta deve seguir
            users_for_this_account = users_per_account
            if i < remaining_users:
                users_for_this_account += 1
                
            # Limitar pelo máximo permitido
            users_for_this_account = min(users_for_this_account, max_follows_per_account)
            
            # Pegar usuários para esta conta
            account_targets = target_usernames[user_index:user_index + users_for_this_account]
            user_index += users_for_this_account
            
            if not account_targets:
                continue
                
            print(f"\n{Fore.CYAN}=== Usando conta: {account['username']} ==={Style.RESET_ALL}")
            print(f"Seguidas planejadas: {len(account_targets)}")
            
            # Usar a conta para seguir
            account_result = self._follow_with_single_account(
                account, account_targets
            )
            
            results['account_results'][account['username']] = account_result
            results['accounts_used'] += 1
            results['total_follows'] += account_result.get('successful_follows', 0)
            
            # Delay entre contas (exceto na última)
            if i < len(active_accounts) - 1 and user_index < len(target_usernames):
                delay = random.uniform(delay_between_accounts[0], delay_between_accounts[1])
                print(f"{Fore.YELLOW}Aguardando {delay:.1f} segundos antes da próxima conta...{Style.RESET_ALL}")
                time.sleep(delay)
                
        return results
        
    def _follow_with_single_account(self, account: Dict, target_usernames: List[str]) -> Dict:
        """
        Usa uma única conta para seguir usuários
        
        Args:
            account: Dados da conta
            target_usernames: Lista de usuários a seguir
            
        Returns:
            Resultado da operação
        """
        result = {
            'account': account['username'],
            'targets': target_usernames,
            'successful_follows': 0,
            'failed_follows': 0,
            'errors': []
        }
        
        try:
            with InstagramAutomation(headless=False, debug=True) as automation:
                # Fazer login
                if not automation.login(account['username'], account['password']):
                    result['errors'].append("Falha no login")
                    self.update_account_status(account['username'], 'error')
                    return result
                    
                # Seguir usuários
                follow_results = automation.follow_multiple_users(
                    target_usernames, 
                    delay_range=(3, 8)
                )
                
                # Contar resultados
                for username, success in follow_results.items():
                    if success:
                        result['successful_follows'] += 1
                    else:
                        result['failed_follows'] += 1
                        
                # Atualizar status da conta
                if result['successful_follows'] > 0:
                    self.update_account_status(
                        account['username'], 
                        'active', 
                        account.get('follow_count', 0) + result['successful_follows']
                    )
                    
        except Exception as e:
            error_msg = f"Erro na conta {account['username']}: {str(e)}"
            result['errors'].append(error_msg)
            self.logger.error(error_msg)
            self.update_account_status(account['username'], 'error')
            
        return result
        
    def create_sample_config(self):
        """Cria arquivo de configuração de exemplo"""
        sample_data = {
            'accounts': [
                {
                    'username': 'sua_conta_1',
                    'password': 'sua_senha_1',
                    'enabled': True,
                    'last_used': None,
                    'follow_count': 0,
                    'status': 'active'
                },
                {
                    'username': 'sua_conta_2',
                    'password': 'sua_senha_2',
                    'enabled': True,
                    'last_used': None,
                    'follow_count': 0,
                    'status': 'active'
                }
            ],
            'last_updated': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, indent=2, ensure_ascii=False)
            
        print(f"{Fore.GREEN}Arquivo de exemplo criado: {self.config_file}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Edite o arquivo com suas credenciais reais antes de usar!{Style.RESET_ALL}")