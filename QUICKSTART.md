# ⚡ Guia de Início Rápido - TaleSeed API

Coloque a API funcionando em **3 minutos**!

---

## 📦 Instalação Rápida

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Configurar API Key

Crie um arquivo `.env`:
```env
GEMINI_API_KEY=sua_chave_aqui
```

> 🔑 **Obter chave:** https://makersuite.google.com/app/apikey

### 3. Iniciar API
```bash
python main.py
```

Ou no Windows:
```bash
start.bat
```

✅ API rodando em: `http://localhost:8000`

---

## 🧪 Teste Rápido

### Abra o navegador:
```
http://localhost:8000/docs
```

### Ou use Python:

```python
import requests

# Teste básico
response = requests.get("http://localhost:8000/health")
print(response.json())
# Saída: {"status": "healthy", "service": "TaleSeed API"}

# Gerar um capítulo
chapter = requests.post("http://localhost:8000/generate-chapter", json={
    "projectId": "test",
    "chapterId": "ch1",
    "projectTitle": "Minha História",
    "chapterTitle": "Capítulo 1",
    "chapterSummary": "O início da aventura",
    "keyPoints": ["Apresentar herói"],
    "tone": "aventureiro",
    "writingStyle": "narrativo",
    "setting": "floresta mística",
    "lengthInPages": 2,
    "previousChapters": [],
    "mode": "single",
    "language": "pt-BR"
})

print(chapter.json()["text"])
```

---

## 📡 Endpoints Principais

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/generate-chapter` | Gera capítulo completo |
| POST | `/creative-suggestions` | Gera sugestões criativas |
| GET | `/health` | Status da API |

---

## 💡 Exemplos Rápidos

### Gerar Sugestões de Títulos
```python
import requests

suggestions = requests.post("http://localhost:8000/creative-suggestions", json={
    "type": "title",
    "context": "Uma história sobre piratas espaciais",
    "genre": "ficção científica",
    "tone": "aventureiro",
    "count": 5
})

for s in suggestions.json()["suggestions"]:
    print(f"• {s['text']}")
```

### Gerar Nomes de Personagens
```python
import requests

chars = requests.post("http://localhost:8000/creative-suggestions", json={
    "type": "character",
    "context": "Detetive em cidade noir",
    "genre": "policial",
    "tone": "sombrio",
    "count": 3
})

for c in chars.json()["suggestions"]:
    print(f"👤 {c['text']}")
```

---

## 🔧 Configuração (Opcional)

Edite `.env` para customizar:

```env
# Modelo (flash = rápido, pro = melhor qualidade)
GEMINI_MODEL=gemini-1.5-flash

# Nível de log
LOG_LEVEL=INFO

# Criatividade (0.0 = conservador, 1.0 = criativo)
TEMPERATURE=0.7

# Tokens máximos na resposta
MAX_OUTPUT_TOKENS=8192

# Porta da API
PORT=8000
```

---

## 🐛 Problemas Comuns

### "GEMINI_API_KEY não encontrada"
➜ Crie o arquivo `.env` com sua chave

### "Módulo não encontrado"
➜ Execute: `pip install -r requirements.txt`

### Porta 8000 em uso
➜ Mude no `.env`: `PORT=8001`

---

## 📚 Próximos Passos

- ✅ Veja exemplos completos: [EXAMPLES.md](EXAMPLES.md)
- ✅ Leia documentação completa: [README.md](README.md)
- ✅ Acesse Swagger UI: `http://localhost:8000/docs`

---

## 🚀 Pronto!

Agora você pode começar a gerar conteúdo literário com IA!

**Dúvidas?** Abra uma issue ou consulte a documentação.
