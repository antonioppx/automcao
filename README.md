# 🤖 Instagram Follow Bot

Automação para seguir usuários específicos usando múltiplas contas do Instagram de forma rápida e eficiente.

## ⚠️ AVISO IMPORTANTE

Este software é para fins educacionais. Use com responsabilidade e respeite os Termos de Serviço do Instagram. O uso inadequado pode resultar em suspensão das contas.

## 🚀 Funcionalidades

- ✅ Gerenciamento de múltiplas contas do Instagram
- ✅ Follow automático de usuários específicos
- ✅ Execução sequencial ou paralela
- ✅ Sistema de delays para evitar detecção
- ✅ Logs detalhados de todas as operações
- ✅ Interface de linha de comando intuitiva
- ✅ Estatísticas de uso por conta
- ✅ Configurações personalizáveis

## 📋 Pré-requisitos

- Python 3.7 ou superior
- Google Chrome instalado
- Contas do Instagram válidas

## 🛠️ Instalação

1. **Clone ou baixe os arquivos** para uma pasta no seu computador

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute o programa:**
   ```bash
   python main.py
   ```

## 📖 Como Usar

### 1. Primeira Execução

Na primeira execução, o programa criará um arquivo `accounts.json` com exemplos. Edite este arquivo com suas contas reais:

```json
[
  {
    "username": "sua_conta_1",
    "password": "sua_senha_1", 
    "account_id": "conta_1",
    "active": true,
    "last_used": null,
    "follows_today": 0
  }
]
```

### 2. Menu Principal

O programa oferece um menu interativo com as seguintes opções:

- **Gerenciar contas**: Adicionar, remover e listar contas
- **Executar follow automático**: Seguir usuários específicos
- **Configurações**: Ver configurações atuais
- **Ver estatísticas**: Acompanhar performance das contas

### 3. Executando Follows

1. Escolha "Executar follow automático" no menu
2. Digite os usernames dos usuários que deseja seguir (separados por vírgula)
3. Escolha o modo de execução:
   - **Sequencial**: Uma conta por vez (mais seguro)
   - **Paralelo**: Todas as contas simultaneamente (mais rápido)
4. Defina quantas contas usar (opcional)
5. Confirme a operação

## ⚙️ Configurações

Edite o arquivo `config.py` para personalizar:

```python
# Delays para evitar detecção
MIN_DELAY = 2  # segundos
MAX_DELAY = 5  # segundos

# Limites de follow
MAX_FOLLOWS_PER_ACCOUNT = 50  # máximo por conta por sessão
FOLLOW_DELAY_MIN = 3  # delay mínimo entre follows
FOLLOW_DELAY_MAX = 8  # delay máximo entre follows

# Navegador
HEADLESS = False  # True para executar sem interface gráfica
```

## 📁 Estrutura de Arquivos

```
automação insta/
├── main.py              # Script principal
├── instagram_bot.py     # Classe principal do bot
├── account_manager.py   # Gerenciador de contas
├── config.py           # Configurações
├── requirements.txt    # Dependências
├── accounts.json       # Contas cadastradas (criado automaticamente)
├── logs/              # Logs de execução (criado automaticamente)
└── README.md          # Este arquivo
```

## 📊 Logs e Monitoramento

- Todos os logs são salvos na pasta `logs/`
- Cada conta tem seu próprio arquivo de log
- Logs incluem timestamps e detalhes de todas as operações
- Estatísticas são atualizadas automaticamente

## 🛡️ Recursos de Segurança

- **Delays aleatórios** entre ações
- **User agents aleatórios** para cada sessão
- **Digitação humana simulada**
- **Limites de follows** por conta
- **Detecção de erros** e recuperação
- **Logs detalhados** para monitoramento

## 🔧 Solução de Problemas

### Erro de Login
- Verifique se o username e senha estão corretos
- Algumas contas podem precisar de verificação 2FA
- Contas muito novas podem ter limitações

### Navegador não inicia
- Verifique se o Google Chrome está instalado
- Execute como administrador se necessário
- Verifique se não há outros processos do Chrome rodando

### Follows não funcionam
- Verifique se os usernames estão corretos
- Alguns perfis podem estar privados
- Contas podem ter atingido limites de follow

## 📈 Dicas de Uso

1. **Comece devagar**: Use poucas contas inicialmente
2. **Monitore os logs**: Acompanhe o desempenho das contas
3. **Use delays adequados**: Não seja muito agressivo
4. **Diversifique horários**: Evite usar sempre no mesmo horário
5. **Mantenha contas ativas**: Use as contas regularmente

## ⚖️ Termos de Uso

- Use este software por sua própria conta e risco
- Respeite os Termos de Serviço do Instagram
- Não use para spam ou atividades maliciosas
- Mantenha backups das suas contas
- Use com moderação para evitar suspensões

## 🆘 Suporte

Para problemas ou dúvidas:
1. Verifique os logs na pasta `logs/`
2. Consulte a seção de solução de problemas
3. Verifique se todas as dependências estão instaladas
4. Teste com uma conta primeiro antes de usar múltiplas

## 📝 Changelog

### v1.0.0
- Lançamento inicial
- Suporte a múltiplas contas
- Follow automático
- Sistema de logs
- Interface de linha de comando
- Configurações personalizáveis

---

**Desenvolvido com ❤️ para automação responsável do Instagram**