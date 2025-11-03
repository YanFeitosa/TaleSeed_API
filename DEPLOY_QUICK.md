# 🚀 Deploy Rápido - 5 Minutos

## Opção 1: Render (MAIS FÁCIL) ⭐

### 1. Subir para GitHub

```bash
# Se ainda não tem repositório
git init
git add .
git commit -m "TaleSeed API ready for deploy"
git branch -M main

# Crie um repositório no GitHub e depois:
git remote add origin https://github.com/SEU_USUARIO/taleseed-api.git
git push -u origin main
```

### 2. Deploy no Render

1. Acesse: https://render.com
2. Clique em "Get Started for Free"
3. Conecte sua conta GitHub
4. Clique em "New +" → "Web Service"
5. Selecione seu repositório `taleseed-api`
6. O Render detecta automaticamente o `render.yaml`!
7. Adicione apenas a variável secreta:
   - `GEMINI_API_KEY` = sua_chave_aqui
8. Clique em "Create Web Service"

### 3. Pronto! ✅

Sua API estará em: `https://taleseed-api.onrender.com`

Teste: `https://taleseed-api.onrender.com/docs`

---

## Opção 2: Railway (TAMBÉM FÁCIL)

### 1. Deploy

1. Acesse: https://railway.app
2. "Start a New Project"
3. "Deploy from GitHub repo"
4. Selecione seu repositório
5. Adicione variáveis:
   - `GEMINI_API_KEY` = sua_chave
   - `GEMINI_MODEL` = gemini-1.5-flash
   - `PORT` = 8000
6. Deploy automático!

### 2. Pronto! ✅

URL: `https://taleseed-api.up.railway.app`

---

## ⚠️ Importante

### Antes do Deploy:

✅ Arquivo `.env` está no `.gitignore`
✅ Teste local: `python main.py`
✅ Arquivo `requirements.txt` atualizado

### Após o Deploy:

✅ Configure variáveis de ambiente
✅ Teste endpoint: `/health`
✅ Teste endpoint: `/docs`
✅ Teste geração: `/generate-chapter`

---

## 🐛 Problemas?

### Render hiberna?
→ Use https://uptimerobot.com
→ Configure ping a cada 10 min

### Erro ao iniciar?
→ Veja os logs no dashboard
→ Verifique `GEMINI_API_KEY`

### API lenta?
→ Normal no primeiro request (hibernação)
→ Segunda request é rápida

---

## 📝 Checklist de Deploy

- [ ] Código no GitHub
- [ ] `.env` NÃO commitado
- [ ] Conta criada na plataforma
- [ ] Repositório conectado
- [ ] Variáveis configuradas
- [ ] Deploy finalizado
- [ ] `/health` funcionando
- [ ] `/docs` acessível
- [ ] Teste de geração OK

---

## 🎉 Próximos Passos

1. Compartilhe sua API
2. Documente a URL
3. Configure monitoramento
4. Adicione domínio customizado (opcional)

**URL da sua API:** `https://_____.onrender.com`

**Boa sorte! 🚀**
