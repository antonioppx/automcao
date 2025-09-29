#!/usr/bin/env python3
"""
Interface Web para Instagram Automation
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, login_user, login_required, logout_user,
    current_user, UserMixin
)
import json
import os
import threading
import time
from datetime import datetime
from account_manager import AccountManager
from instagram_automation import InstagramAutomation
import logging

app = Flask(__name__)
app.secret_key = 'instagram_automation_secret_key_2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ==========================
# Modelos
# ==========================
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # simples (hash recomendado)

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    account_id = db.Column(db.String(120), nullable=False)
    enabled = db.Column(db.Boolean, default=True)
    last_used = db.Column(db.String(64))
    follow_count = db.Column(db.Integer, default=0)
    status = db.Column(db.String(32), default='active')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar gerenciador de contas
account_manager = AccountManager()
# Carrega contas na importação para funcionar quando iniciado via start_web.py
try:
    account_manager.load_accounts()
except Exception:
    pass

# Utilitário: converter contas do banco para lista de dicionários
def get_accounts_list():
    rows = Account.query.order_by(Account.username.asc()).all()
    accounts = []
    for r in rows:
        accounts.append({
            'username': r.username,
            'password': r.password,
            'account_id': r.account_id,
            'enabled': r.enabled,
            'last_used': r.last_used,
            'follow_count': r.follow_count,
            'status': r.status
        })
    return accounts

# Status global da execução
execution_status = {
    'running': False,
    'current_account': None,
    'progress': 0,
    'total_targets': 0,
    'completed_targets': 0,
    'results': {},
    'start_time': None,
    'end_time': None
}

@app.route('/')
def index():
    """Redireciona para login ou home conforme sessão"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    """Página principal após login"""
    return render_template('index.html')

@app.route('/accounts')
@login_required
def accounts():
    """Página de gerenciamento de contas"""
    accounts_data = get_accounts_list()
    return render_template('accounts.html', accounts=accounts_data)

@app.route('/add_account', methods=['POST'])
@login_required
def add_account():
    """Adicionar nova conta"""
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        account_id = request.form.get('account_id', username)
        
        if not username or not password:
            flash('Username e senha são obrigatórios!', 'error')
            return redirect(url_for('accounts'))
        
        # Persistir no banco
        exists = Account.query.filter_by(username=username).first()
        if exists:
            flash(f'Conta {username} já existe!', 'error')
        else:
            row = Account(
                username=username,
                password=password,
                account_id=account_id or username,
                enabled=True
            )
            db.session.add(row)
            db.session.commit()
            flash(f'Conta {username} adicionada com sucesso!', 'success')
            
    except Exception as e:
        flash(f'Erro: {str(e)}', 'error')
    
    return redirect(url_for('accounts'))

@app.route('/remove_account/<username>')
@login_required
def remove_account(username):
    """Remover conta"""
    try:
        row = Account.query.filter_by(username=username).first()
        if not row:
            flash(f'Conta {username} não encontrada!', 'error')
        else:
            db.session.delete(row)
            db.session.commit()
            flash(f'Conta {username} removida com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro: {str(e)}', 'error')
    
    return redirect(url_for('accounts'))

@app.route('/follow')
@login_required
def follow():
    """Página de execução de follows"""
    active_accounts = [a for a in get_accounts_list() if a.get('enabled', True)]
    return render_template('follow.html', accounts=active_accounts)

@app.route('/start_follow', methods=['POST'])
@login_required
def start_follow():
    """Iniciar processo de follow"""
    global execution_status
    
    if execution_status['running']:
        return jsonify({'success': False, 'message': 'Já existe uma execução em andamento!'})
    
    try:
        # Obter dados do formulário
        target_usernames = request.form.get('target_usernames', '').strip()
        max_follows = int(request.form.get('max_follows', 10))
        execution_mode = request.form.get('mode', 'sequential')
        
        if not target_usernames:
            return jsonify({'success': False, 'message': 'Nenhum usuário alvo especificado!'})
        
        # Processar lista de usuários
        targets = [u.strip() for u in target_usernames.split(',') if u.strip()]
        
        if not targets:
            return jsonify({'success': False, 'message': 'Nenhum usuário válido encontrado!'})
        
        # Verificar contas ativas
        active_accounts = [a for a in get_accounts_list() if a.get('enabled', True)]
        if not active_accounts:
            return jsonify({'success': False, 'message': 'Nenhuma conta ativa encontrada!'})
        
        # Inicializar status
        execution_status.update({
            'running': True,
            'current_account': None,
            'progress': 0,
            'total_targets': len(targets),
            'completed_targets': 0,
            'results': {},
            'start_time': datetime.now().isoformat(),
            'end_time': None
        })
        
        # Iniciar execução em thread separada
        thread = threading.Thread(
            target=execute_follow_process,
            args=(targets, max_follows, execution_mode)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({'success': True, 'message': 'Execução iniciada com sucesso!'})
        
    except Exception as e:
        logger.error(f"Erro ao iniciar follow: {str(e)}")
        return jsonify({'success': False, 'message': f'Erro: {str(e)}'})

def execute_follow_process(targets, max_follows, mode):
    """Executar processo de follow em thread separada"""
    global execution_status
    # Garantir contexto da aplicação dentro da thread
    with app.app_context():
        try:
            if mode == 'sequential':
                execute_sequential_follow(targets, max_follows)
            else:
                execute_parallel_follow(targets, max_follows)
        except Exception as e:
            logger.error(f"Erro durante execução: {str(e)}")
        finally:
            execution_status['running'] = False
            execution_status['end_time'] = datetime.now().isoformat()

def execute_sequential_follow(targets, max_follows):
    """Executar follows sequencialmente"""
    global execution_status
    
    active_accounts = [a for a in get_accounts_list() if a.get('enabled', True)]
    
    for i, account in enumerate(active_accounts):
        if not execution_status['running']:
            break
            
        execution_status['current_account'] = account['username']
        
        try:
            with InstagramAutomation(headless=False, debug=True) as automation:
                # Login
                if not automation.login(account['username'], account['password']):
                    execution_status['results'][account['username']] = {
                        'success': False,
                        'error': 'Falha no login'
                    }
                    continue
                
                # Seguir usuários
                account_targets = targets[:max_follows]
                follow_results = automation.follow_multiple_users(account_targets)
                
                # Contar resultados
                successful = sum(1 for success in follow_results.values() if success)
                failed = len(follow_results) - successful
                
                execution_status['results'][account['username']] = {
                    'success': True,
                    'successful_follows': successful,
                    'failed_follows': failed,
                    'targets': list(follow_results.keys())
                }
                
                execution_status['completed_targets'] += successful
                execution_status['progress'] = int((execution_status['completed_targets'] / 
                                                  execution_status['total_targets']) * 100)
                
        except Exception as e:
            execution_status['results'][account['username']] = {
                'success': False,
                'error': str(e)
            }
        
        # Delay entre contas
        if i < len(active_accounts) - 1:
            time.sleep(30)

def execute_parallel_follow(targets, max_follows):
    """Executar follows em paralelo"""
    global execution_status
    
    active_accounts = [a for a in get_accounts_list() if a.get('enabled', True)]
    threads = []
    
    def follow_worker(account):
        # Cada worker também precisa do contexto da aplicação
        with app.app_context():
            try:
                with InstagramAutomation(headless=False, debug=True) as automation:
                    if not automation.login(account['username'], account['password']):
                        execution_status['results'][account['username']] = {
                            'success': False,
                            'error': 'Falha no login'
                        }
                        return
                    
                    account_targets = targets[:max_follows]
                    follow_results = automation.follow_multiple_users(account_targets)
                    
                    successful = sum(1 for success in follow_results.values() if success)
                    failed = len(follow_results) - successful
                    
                    execution_status['results'][account['username']] = {
                        'success': True,
                        'successful_follows': successful,
                        'failed_follows': failed,
                        'targets': list(follow_results.keys())
                    }
            except Exception as e:
                execution_status['results'][account['username']] = {
                    'success': False,
                    'error': str(e)
                }
    
    # Iniciar threads
    for account in active_accounts:
        thread = threading.Thread(target=follow_worker, args=(account,))
        threads.append(thread)
        thread.start()
        time.sleep(5)  # Delay entre iniciação das threads
    
    # Aguardar todas as threads
    for thread in threads:
        thread.join()

@app.route('/status')
@login_required
def get_status():
    """Obter status da execução"""
    return jsonify(execution_status)

@app.route('/stop_execution')
@login_required
def stop_execution():
    """Parar execução"""
    global execution_status
    execution_status['running'] = False
    return jsonify({'success': True, 'message': 'Execução parada!'})

@app.route('/logs')
@login_required
def logs():
    """Página de logs"""
    log_files = []
    logs_dir = 'logs'
    
    if os.path.exists(logs_dir):
        for file in os.listdir(logs_dir):
            if file.endswith('.log'):
                log_files.append(file)
    
    return render_template('logs.html', log_files=log_files)

@app.route('/view_log/<filename>')
@login_required
def view_log(filename):
    """Visualizar arquivo de log"""
    log_path = os.path.join('logs', filename)
    
    if not os.path.exists(log_path):
        flash('Arquivo de log não encontrado!', 'error')
        return redirect(url_for('logs'))
    
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return render_template('view_log.html', filename=filename, content=content)
    except Exception as e:
        flash(f'Erro ao ler log: {str(e)}', 'error')
        return redirect(url_for('logs'))

@app.route('/stats')
@login_required
def stats():
    """Página de estatísticas"""
    accounts_data = get_accounts_list()
    
    total_accounts = len(accounts_data)
    active_accounts = len([acc for acc in accounts_data if acc.get('enabled', True)])
    total_follows = sum(acc.get('follow_count', 0) for acc in accounts_data)
    
    stats_data = {
        'total_accounts': total_accounts,
        'active_accounts': active_accounts,
        'total_follows': total_follows,
        'accounts': accounts_data
    }
    
    return render_template('stats.html', stats=stats_data)

# ==========================
# Autenticação
# ==========================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('index'))
        flash('Credenciais inválidas', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Carregar contas existentes
    account_manager.load_accounts()
    
    # Criar diretório de templates se não existir
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Criar diretório de logs se não existir
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    print("🚀 Iniciando Instagram Automation Web Interface...")
    print("📱 Acesse: http://localhost:5000")
    print("🛑 Para parar: Ctrl+C")
    
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
