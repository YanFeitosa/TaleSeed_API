# 🌐 Deploy Gratuito - TaleSeed API

Guia completo para colocar sua API online gratuitamente.

---

## 🎯 Melhores Opções Gratuitas

### 1. 🚀 Render (RECOMENDADO)
**✅ Melhor opção geral**

#### Por que escolher:
- ✅ 750 horas/mês grátis
- ✅ Deploy automático do GitHub
- ✅ HTTPS gratuito
- ✅ Muito fácil de configurar
- ✅ Suporta variáveis de ambiente
- ⚠️ Hiberna após 15 min de inatividade (primeiro request lento)

#### Como fazer:

**Passo 1: Criar arquivo `render.yaml`**
```yaml
services:
  - type: web
    name: taleseed-api
    runtime: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: GEMINI_API_KEY
        sync: false
      - key: GEMINI_MODEL
        value: gemini-1.5-flash
      - key: LOG_LEVEL
        value: INFO
      - key: TEMPERATURE
        value: "0.7"
      - key: MAX_OUTPUT_TOKENS
        value: "8192"
```

**Passo 2: Deploy**
1. Crie conta em https://render.com
2. Conecte seu repositório GitHub
3. Crie novo "Web Service"
4. Selecione seu repositório
5. Configure as variáveis de ambiente
6. Clique em "Deploy"

**Acesso:** `https://taleseed-api.onrender.com`

---

### 2. 🐍 PythonAnywhere
**✅ Bom para Python**

#### Por que escolher:
- ✅ Sempre online (não hiberna)
- ✅ 100MB de espaço
- ✅ Gratuito para sempre
- ⚠️ Configuração mais manual
- ⚠️ Limite de CPU diário

#### Como fazer:

**Passo 1: Criar conta**
- Acesse https://www.pythonanywhere.com
- Crie uma conta gratuita

**Passo 2: Upload dos arquivos**
```bash
# Via Git
git clone https://github.com/seu-usuario/taleseed-api.git
cd taleseed-api
pip install -r requirements.txt
```

**Passo 3: Configurar WSGI**
Edite `/var/www/seu_usuario_pythonanywhere_com_wsgi.py`:
```python
import sys
import os

path = '/home/seu_usuario/taleseed-api'
if path not in sys.path:
    sys.path.append(path)

# Carrega variáveis de ambiente
from dotenv import load_dotenv
load_dotenv('/home/seu_usuario/taleseed-api/.env')

from main import app as application
```

**Acesso:** `https://seu_usuario.pythonanywhere.com`

---

### 3. ☁️ Railway
**✅ Muito fácil**

#### Por que escolher:
- ✅ $5 grátis/mês (500 horas)
- ✅ Deploy super rápido
- ✅ Não hiberna
- ✅ Integração com GitHub
- ⚠️ Depois de $5, precisa pagar

#### Como fazer:

**Passo 1: Criar `Procfile`**
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Passo 2: Deploy**
1. Acesse https://railway.app
2. "Start a New Project"
3. "Deploy from GitHub"
4. Selecione seu repositório
5. Adicione variáveis de ambiente
6. Deploy automático!

**Acesso:** `https://taleseed-api.up.railway.app`

---

### 4. 🔷 Deta Space
**✅ Boa para APIs pequenas**

#### Por que escolher:
- ✅ Completamente grátis
- ✅ Muito rápido
- ✅ Não hiberna
- ⚠️ Limite de 10GB transferência/mês

#### Como fazer:

**Passo 1: Instalar Deta CLI**
```bash
curl -fsSL https://get.deta.dev/cli.sh | sh
```

**Passo 2: Criar `Spacefile`**
```yaml
v: 0
micros:
  - name: taleseed-api
    src: .
    engine: python3.9
    run: uvicorn main:app
    dev: uvicorn main:app --reload
```

**Passo 3: Deploy**
```bash
deta login
deta new
deta deploy
```

---

### 5. 🔶 Vercel
**⚠️ Requer adaptação**

#### Por que escolher:
- ✅ Muito rápido (Edge)
- ✅ Deploy automático
- ⚠️ Precisa adaptar para serverless

#### Como fazer:

**Passo 1: Criar `vercel.json`**
```json
{
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ]
}
```

**Passo 2: Adaptar `main.py`**
```python
# Adicionar no final
app = app  # Para Vercel
```

**Passo 3: Deploy**
```bash
npm i -g vercel
vercel
```

---

## 📋 Comparação Rápida

| Plataforma | Preço | Sempre Online | Facilidade | Limite |
|------------|-------|---------------|------------|--------|
| **Render** | Grátis | ⚠️ Hiberna | ⭐⭐⭐⭐⭐ | 750h/mês |
| **PythonAnywhere** | Grátis | ✅ Sim | ⭐⭐⭐ | CPU diário |
| **Railway** | $5/mês | ✅ Sim | ⭐⭐⭐⭐⭐ | 500h grátis |
| **Deta** | Grátis | ✅ Sim | ⭐⭐⭐⭐ | 10GB/mês |
| **Vercel** | Grátis | ✅ Sim | ⭐⭐⭐ | Serverless |

---

## 🏆 Recomendação por Caso de Uso

### Para Testes/MVP
→ **Render** (mais fácil, grátis, suficiente)

### Para Produção (baixo tráfego)
→ **Railway** ou **PythonAnywhere**

### Para Produção (alto tráfego)
→ **Deta** ou **Railway** (pago)

### Para Performance Máxima
→ **Vercel** (mas precisa adaptar)

---

## 🚀 Deploy Rápido no Render (RECOMENDADO)

### Passo a Passo Completo:

**1. Preparar Repositório**

Crie arquivo `render.yaml`:
```yaml
services:
  - type: web
    name: taleseed-api
    runtime: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /health
```

**2. Criar `.gitignore`**
```
__pycache__/
*.pyc
.env
venv/
```

**3. Push para GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/seu-usuario/taleseed-api.git
git push -u origin main
```

**4. Deploy no Render**
1. Acesse https://render.com
2. Clique em "Get Started"
3. Conecte sua conta GitHub
4. "New +" → "Web Service"
5. Selecione seu repositório
6. Configure:
   - **Name:** taleseed-api
   - **Runtime:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
7. Adicione variáveis de ambiente:
   - `GEMINI_API_KEY` = sua_chave
   - `GEMINI_MODEL` = gemini-1.5-flash
   - `LOG_LEVEL` = INFO
   - `TEMPERATURE` = 0.7
   - `MAX_OUTPUT_TOKENS` = 8192
8. Clique em "Create Web Service"

**5. Aguarde o Deploy** (2-5 minutos)

**6. Acesse sua API!**
```
https://taleseed-api.onrender.com/docs
```

---

## 📝 Dicas Importantes

### 1. Variáveis de Ambiente
- ⚠️ **NUNCA** faça commit do `.env`
- ✅ Configure na plataforma de deploy
- ✅ Use `.env.example` como referência

### 2. Performance
- ⚠️ Render hiberna após 15 min
- ✅ Solução: Use um serviço de "ping" como [UptimeRobot](https://uptimerobot.com)
- ✅ Configure para fazer request a cada 10 min

### 3. Logs
- ✅ Todas as plataformas têm visualização de logs
- ✅ Use para debugar problemas

### 4. HTTPS
- ✅ Todas as opções incluem HTTPS gratuito
- ✅ Seus certificados são gerenciados automaticamente

### 5. Domínio Customizado
- ✅ A maioria permite domínio próprio (grátis)
- ✅ Configure no painel da plataforma

---

## 🔧 Solução de Problemas

### "Application failed to start"
→ Verifique os logs
→ Confirme que `requirements.txt` está correto
→ Teste localmente: `uvicorn main:app`

### "Environment variable not found"
→ Verifique se configurou `GEMINI_API_KEY`
→ Restart o serviço após adicionar variáveis

### "Port already in use"
→ Use `$PORT` no comando start
→ Não fixe a porta no código

### API muito lenta
→ Normal na primeira request (hibernação)
→ Use serviço de ping para manter ativa

---

## 🎯 Próximos Passos

Após o deploy:

1. ✅ Teste todos os endpoints
2. ✅ Configure monitoramento (UptimeRobot)
3. ✅ Adicione domínio customizado (opcional)
4. ✅ Configure limites de rate (opcional)
5. ✅ Documente sua URL pública

---

## 📞 Recursos

- **Render:** https://render.com/docs
- **PythonAnywhere:** https://help.pythonanywhere.com
- **Railway:** https://docs.railway.app
- **Deta:** https://deta.space/docs
- **Vercel:** https://vercel.com/docs

---

**Boa sorte com seu deploy! 🚀**
