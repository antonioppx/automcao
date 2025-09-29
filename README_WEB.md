# 🌐 Instagram Automation - Interface Web

Interface web moderna e intuitiva para automação de seguidas no Instagram.

## 🚀 **COMO USAR A INTERFACE WEB**

### **1. Iniciar a Interface Web**

**Opção A - Script Automático (Recomendado):**
```bash
python start_web.py
```

**Opção B - Arquivo Batch (Windows):**
```bash
start_web.bat
```

**Opção C - Manual:**
```bash
python web_app.py
```

### **2. Acessar a Interface**

- **URL Local:** http://localhost:5000
- **URL Rede:** http://SEU_IP:5000 (para acessar de outros dispositivos)

## 📱 **FUNCIONALIDADES DA INTERFACE**

### **🏠 Página Inicial**
- Visão geral do sistema
- Status da execução em tempo real
- Acesso rápido às principais funcionalidades

### **👥 Gerenciar Contas**
- ✅ Adicionar novas contas do Instagram
- ✅ Remover contas existentes
- ✅ Visualizar status de todas as contas
- ✅ Estatísticas por conta

### **❤️ Executar Follows**
- ✅ Configurar usuários alvo
- ✅ Escolher modo de execução (Sequencial/Paralelo)
- ✅ Definir limites de seguidas
- ✅ Monitoramento em tempo real
- ✅ Parar execução a qualquer momento

### **📊 Estatísticas**
- ✅ Gráficos de performance
- ✅ Resumo de todas as contas
- ✅ Métricas detalhadas
- ✅ Histórico de atividades

### **📝 Logs**
- ✅ Visualizar logs em tempo real
- ✅ Buscar em logs
- ✅ Download de arquivos de log
- ✅ Auto-scroll para acompanhar execução

## 🎨 **CARACTERÍSTICAS DA INTERFACE**

### **Design Moderno**
- 🎨 Interface responsiva (funciona em celular, tablet, desktop)
- 🌈 Cores do Instagram (rosa/roxo)
- ⚡ Animações suaves
- 📱 Design mobile-first

### **Experiência do Usuário**
- 🔄 Atualizações em tempo real
- 📊 Gráficos interativos
- 🔍 Busca avançada em logs
- ⚠️ Alertas e confirmações
- 📈 Progresso visual

### **Funcionalidades Avançadas**
- 🚀 Execução em background
- 📡 Monitoramento via AJAX
- 💾 Auto-save de configurações
- 🔒 Validação de dados
- 🛡️ Tratamento de erros

## 🛠️ **CONFIGURAÇÕES**

### **Porta do Servidor**
Por padrão, a interface roda na porta 5000. Para alterar:

```python
# No arquivo web_app.py, linha final:
app.run(debug=True, host='0.0.0.0', port=5000)  # Altere a porta aqui
```

### **Acesso em Rede**
Para acessar de outros dispositivos na mesma rede:

1. Descubra seu IP: `ipconfig` (Windows) ou `ifconfig` (Linux/Mac)
2. Acesse: `http://SEU_IP:5000`
3. Exemplo: `http://192.168.1.100:5000`

## 📋 **REQUISITOS**

- ✅ Python 3.7+
- ✅ Flask (instalado automaticamente)
- ✅ Google Chrome
- ✅ Contas do Instagram válidas

## 🔧 **SOLUÇÃO DE PROBLEMAS**

### **Erro: "ModuleNotFoundError: No module named 'flask'"**
```bash
pip install flask
```

### **Erro: "Address already in use"**
A porta 5000 está ocupada. Altere a porta no arquivo `web_app.py`.

### **Interface não carrega**
1. Verifique se o Python está rodando
2. Verifique se a porta 5000 está livre
3. Tente acessar http://127.0.0.1:5000

### **Chrome não abre automaticamente**
Acesse manualmente: http://localhost:5000

## 🎯 **DICAS DE USO**

### **Para Melhor Performance**
1. Use modo sequencial para contas novas
2. Limite a 10-20 seguidas por conta
3. Monitore os logs regularmente
4. Use delays adequados

### **Para Segurança**
1. Use contas válidas e ativas
2. Não exagere nas seguidas
3. Monitore o status das contas
4. Faça backup das configurações

## 📱 **ACESSO MOBILE**

A interface é totalmente responsiva e funciona perfeitamente em:
- 📱 Smartphones
- 📱 Tablets
- 💻 Laptops
- 🖥️ Desktops

## 🔄 **ATUALIZAÇÕES EM TEMPO REAL**

A interface atualiza automaticamente:
- ⏱️ Status da execução (a cada 2 segundos)
- 📊 Estatísticas (a cada 5 minutos)
- 📝 Logs (a cada 30 segundos)
- 📈 Progresso das seguidas

## 🎉 **VANTAGENS DA INTERFACE WEB**

### **vs Interface de Linha de Comando**
- ✅ Mais fácil de usar
- ✅ Visualização em tempo real
- ✅ Acesso remoto
- ✅ Interface moderna
- ✅ Gráficos e estatísticas

### **vs Scripts Manuais**
- ✅ Configuração visual
- ✅ Monitoramento contínuo
- ✅ Controle total
- ✅ Logs organizados
- ✅ Estatísticas detalhadas

---

## 🚀 **COMEÇAR AGORA**

1. **Execute:** `python start_web.py`
2. **Acesse:** http://localhost:5000
3. **Configure:** Suas contas do Instagram
4. **Execute:** Seguidas automáticas
5. **Monitore:** Resultados em tempo real

**🎯 Interface web pronta para uso!**
