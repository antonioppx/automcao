# 🚀 Deploy no Heroku - Instagram Automation

## 📋 **Passo a Passo Completo**

### **1. Pré-requisitos**
- ✅ Conta no Heroku (gratuita)
- ✅ Heroku CLI instalado
- ✅ Git configurado
- ✅ Projeto no GitHub

### **2. Instalar Heroku CLI**

**Windows:**
```bash
# Baixe de: https://devcenter.heroku.com/articles/heroku-cli
# Ou via Chocolatey:
choco install heroku-cli
```

**Mac:**
```bash
brew tap heroku/brew && brew install heroku
```

**Linux:**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

### **3. Login no Heroku**
```bash
heroku login
```

### **4. Criar App no Heroku**
```bash
heroku create instagram-automation-seuapp
```

### **5. Configurar Buildpacks**
```bash
heroku buildpacks:set https://github.com/heroku/heroku-buildpack-chromedriver
heroku buildpacks:add https://github.com/heroku/heroku-buildpack-google-chrome
heroku buildpacks:add heroku/python
```

### **6. Adicionar Banco PostgreSQL**
```bash
heroku addons:create heroku-postgresql:mini
```

### **7. Configurar Variáveis de Ambiente**
```bash
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=sua_chave_secreta_aqui
```

### **8. Deploy**
```bash
git add .
git commit -m "feat: configuração para Heroku"
git push heroku main
```

### **9. Abrir App**
```bash
heroku open
```

---

## 🎯 **Deploy Rápido (1 Click)**

### **Opção A - Deploy Button**
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/antonioppx/automcao)

### **Opção B - Heroku Dashboard**
1. Acesse: https://dashboard.heroku.com
2. "New" → "Create new app"
3. Nome: `instagram-automation`
4. "Create app"
5. "Deploy" → "GitHub"
6. Conecte o repositório
7. "Deploy branch"

---

## ⚙️ **Configurações Automáticas**

### **Buildpacks Configurados:**
- ✅ ChromeDriver
- ✅ Google Chrome
- ✅ Python

### **Add-ons:**
- ✅ PostgreSQL Mini (gratuito)

### **Variáveis de Ambiente:**
- ✅ `FLASK_ENV=production`
- ✅ `SECRET_KEY` (gerada automaticamente)
- ✅ `DATABASE_URL` (configurada automaticamente)

---

## 📱 **Acesso após Deploy**

### **URL:**
```
https://instagram-automation-seuapp.herokuapp.com
```

### **Login:**
- **Usuário**: `admin`
- **Senha**: `admin`

---

## 🔧 **Comandos Úteis**

### **Ver Logs:**
```bash
heroku logs --tail
```

### **Executar Comando:**
```bash
heroku run python
```

### **Ver Variáveis:**
```bash
heroku config
```

### **Reiniciar App:**
```bash
heroku restart
```

---

## 🚨 **Limitações do Heroku Free**

### **Sleep Mode:**
- ⚠️ App "dorme" após 30min de inatividade
- ⚠️ Primeiro acesso pode ser lento (wake up)
- ✅ Ativação automática em uso

### **Limites:**
- ✅ 550 horas/mês gratuitas
- ✅ 1 dyno (processo)
- ✅ 512MB RAM

---

## 🎉 **Resultado Final**

**URL Online:** `https://instagram-automation-seuapp.herokuapp.com`

**Funcionalidades:**
- ✅ Interface web completa
- ✅ Banco PostgreSQL
- ✅ Chrome/ChromeDriver
- ✅ Automação Instagram
- ✅ SSL automático
- ✅ Logs em tempo real

**🚀 Deploy no Heroku concluído!**
