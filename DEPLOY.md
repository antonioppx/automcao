# 🚀 Guia de Deploy - Instagram Automation

## 🌐 **Deploy Gratuito na Internet**

### **1. 🟢 Railway (Recomendado)**

**Vantagens:**
- ✅ Gratuito: 500h/mês
- ✅ Deploy automático do GitHub
- ✅ Banco PostgreSQL incluso
- ✅ Domínio personalizado
- ✅ SSL automático

**Como fazer:**
1. Acesse: https://railway.app
2. Faça login com GitHub
3. Clique em "New Project"
4. Selecione "Deploy from GitHub repo"
5. Escolha o repositório `automcao`
6. Railway faz deploy automático
7. URL: `https://seuapp.railway.app`

**Configuração do Banco:**
1. No Railway, vá em "Variables"
2. Adicione: `DATABASE_URL=postgresql://...`
3. O sistema usa PostgreSQL automaticamente

---

### **2. 🔵 Render**

**Vantagens:**
- ✅ Gratuito: 750h/mês
- ✅ Auto-deploy do GitHub
- ✅ Banco PostgreSQL gratuito
- ✅ SSL automático

**Como fazer:**
1. Acesse: https://render.com
2. Faça login com GitHub
3. Clique em "New +"
4. Selecione "Web Service"
5. Conecte o repositório
6. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python start_web.py`
7. Deploy automático

---

### **3. 🟡 Heroku**

**Vantagens:**
- ✅ Gratuito: 550h/mês
- ✅ Fácil configuração
- ✅ Add-ons gratuitos

**Como fazer:**
1. Instale Heroku CLI
2. Faça login: `heroku login`
3. Crie app: `heroku create seuapp`
4. Configure banco: `heroku addons:create heroku-postgresql:mini`
5. Deploy: `git push heroku main`

---

## 📋 **Arquivos de Deploy Inclusos**

### **Procfile**
```
web: python start_web.py
```

### **runtime.txt**
```
python-3.11.0
```

### **railway.json**
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python start_web.py",
    "healthcheckPath": "/",
    "healthcheckTimeout": 300,
    "restartPolicyType": "ON_FAILURE"
  }
}
```

---

## ⚙️ **Configurações para Deploy**

### **Variáveis de Ambiente**
Configure no painel do serviço:

```env
FLASK_ENV=production
DATABASE_URL=postgresql://user:pass@host:port/db
SECRET_KEY=sua_chave_secreta_aqui
```

### **Banco de Dados**
- **Local**: SQLite (`app.db`)
- **Produção**: PostgreSQL (Railway/Render/Heroku)

---

## 🚀 **Deploy Rápido - Railway**

**Passo a passo:**

1. **GitHub**: Código já está no repositório
2. **Railway**: https://railway.app
3. **Login**: Com GitHub
4. **New Project**: Deploy from GitHub
5. **Selecionar**: Repositório `automcao`
6. **Aguardar**: Deploy automático
7. **Acessar**: URL gerada

**URL final:** `https://seuapp.railway.app`

---

## 📱 **Acesso após Deploy**

### **Login Padrão**
- **Usuário**: `admin`
- **Senha**: `admin`

### **Funcionalidades Online**
- ✅ Interface web completa
- ✅ Gerenciar contas Instagram
- ✅ Executar follows automáticos
- ✅ Monitoramento em tempo real
- ✅ Logs e estatísticas

---

## 🔧 **Troubleshooting**

### **Erro de Banco**
- Verifique `DATABASE_URL` nas variáveis
- Railway/Render configuram automaticamente

### **Erro de Porta**
- Código já configurado para usar `PORT` do ambiente
- Funciona automaticamente

### **Erro de Dependências**
- `requirements.txt` já inclui tudo
- Deploy automático instala dependências

---

## 🎯 **Resultado Final**

**URL Online:** `https://seuapp.railway.app`

**Funcionalidades:**
- ✅ Acesso de qualquer lugar
- ✅ Interface web completa
- ✅ Banco de dados online
- ✅ Logs em tempo real
- ✅ SSL seguro

**🎉 Deploy gratuito funcionando!**
