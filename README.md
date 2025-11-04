# 🌱 TaleSeed API

API REST para geração de conteúdo literário usando IA (Google Gemini).

Gera capítulos completos de livros e sugestões criativas (títulos, personagens, enredos, ambientações) usando inteligência artificial.

---

## 🚀 Início Rápido

### 1. Instalar
```bash
pip install -r requirements.txt
```

### 2. Configurar
Crie arquivo `.env`:
```env
GEMINI_API_KEY=sua_chave_aqui
GEMINI_MODEL=gemini-1.5-flash
```

> 🔑 Obter chave: https://makersuite.google.com/app/apikey

### 3. Executar
```bash
python main.py
```

**Acesso:** http://localhost:8000

**Documentação:** http://localhost:8000/docs

---

---

## 📡 Endpoints

### POST /generate-chapter
Gera capítulo completo de livro.

**Request:**
```json
{
  "projectId": "proj_001",
  "chapterId": "ch_001",
  "projectTitle": "Minha História",
  "chapterTitle": "Capítulo 1",
  "chapterSummary": "O início da aventura",
  "keyPoints": ["Apresentar protagonista"],  // opcional
  "tone": "aventureiro",
  "writingStyle": "narrativo",
  "setting": "floresta mística",
  "lengthInPages": 5,
  "previousChapters": [],
  "mode": "single",
  "language": "pt-BR"
}
```

### POST /creative-suggestions
Gera sugestões criativas.

**Tipos:** `title`, `character`, `plot`, `setting`

**Request:**
```json
{
  "type": "title",
  "context": "História sobre piratas espaciais",
  "genre": "ficção científica",
  "tone": "aventureiro",
  "count": 5
}
```

### POST /summarize
Gera resumo estruturado de capítulo focado em continuidade.

**Request:**
```json
{
  "chapterText": "Texto completo do capítulo aqui...",
  "chapterTitle": "Capítulo 1",  // opcional
  "language": "pt-BR"
}
```

**Response:**
```json
{
  "summary": "Resumo narrativo completo do capítulo...",
  "characters": [
    "João Silva (protagonista, detetive)",
    "Maria Santos (testemunha)"
  ],
  "settings": [
    "Café Central da cidade",
    "Delegacia do 5º distrito"
  ],
  "keyEvents": [
    "João recebe chamado sobre crime",
    "Entrevista com testemunha Maria",
    "Descoberta de pista crucial"
  ],
  "endingState": "João sai da delegacia com nova pista. Está determinado mas preocupado...",
  "tokensUsed": 450
}
```

### GET /health
Status da API.

### GET /ping
Rota leve para acordar o servidor (útil para evitar cold start no Render).

---

## � Garantindo Continuidade entre Capítulos

Para melhor continuidade narrativa entre capítulos:

### ✅ Sempre Envie `previousChapters`
```json
{
  "projectId": "proj_001",
  "chapterId": "ch_002",
  "chapterTitle": "Capítulo 2",
  "chapterSummary": "A jornada continua",
  "previousChapters": [
    {
      "title": "Capítulo 1",
      "summary": "Resumo do capítulo anterior",
      "generatedText": "Texto COMPLETO do capítulo 1 aqui..."
    }
  ],
  "tone": "aventureiro",
  "writingStyle": "narrativo",
  "setting": "floresta mística",
  "lengthInPages": 5,
  "mode": "single",
  "language": "pt-BR"
}
```

### 🎯 Dicas Importantes

1. **Inclua o texto completo** dos capítulos anteriores no campo `generatedText`
2. A IA analisa especialmente o **final do capítulo anterior** para garantir transição suave
3. Mantenha **tom, estilo e ambientação consistentes** entre capítulos
4. Use `keyPoints` para guiar eventos específicos que devem continuar do capítulo anterior

### ⚠️ O que a IA Considera

- **Últimos eventos** do capítulo anterior
- **Estado emocional** dos personagens ao final
- **Linha temporal** e sequência de eventos
- **Detalhes e consistência** com o que já foi escrito

---

## � Fluxo Recomendado com /summarize

Para **máxima continuidade** entre capítulos, use este fluxo:

### Passo 1: Gerar Capítulo 1
```bash
POST /generate-chapter
{
  "chapterTitle": "Capítulo 1",
  "chapterSummary": "Início da aventura",
  ...
}
```

### Passo 2: Resumir Capítulo 1
```bash
POST /summarize
{
  "chapterText": "[texto completo do capítulo 1]",
  "chapterTitle": "Capítulo 1"
}
```

**Resposta estruturada:**
```json
{
  "summary": "Resumo rico e detalhado...",
  "characters": ["João (protagonista)", "Maria (aliada)"],
  "settings": ["Floresta Negra", "Cabana abandonada"],
  "keyEvents": ["João acorda", "Encontra Maria", "Descobrem mapa"],
  "endingState": "João e Maria decidem seguir o mapa ao amanhecer..."
}
```

### Passo 3: Gerar Capítulo 2 (com contexto rico)
```bash
POST /generate-chapter
{
  "chapterTitle": "Capítulo 2",
  "chapterSummary": "A jornada começa",
  "previousChapters": [
    {
      "title": "Capítulo 1",
      "summary": "[use o 'summary' do /summarize]",
      "generatedText": "[texto completo do cap 1]"
    }
  ],
  ...
}
```

### 💡 Vantagens deste Fluxo

- ✅ **Resumo rico** com personagens, locais e eventos estruturados
- ✅ **Estado final claro** para continuidade perfeita
- ✅ **Consistência garantida** de nomes e detalhes
- ✅ **Contexto otimizado** para a IA

### 📝 Exemplo de Código Completo

```python
import requests

# 1. Gerar Capítulo 1
chapter1_response = requests.post("http://localhost:8000/generate-chapter", json={
    "projectId": "test",
    "chapterId": "ch1",
    "projectTitle": "A Aventura",
    "chapterTitle": "Capítulo 1: O Despertar",
    "chapterSummary": "Protagonista acorda em lugar desconhecido",
    "tone": "misterioso",
    "writingStyle": "narrativo",
    "setting": "floresta sombria",
    "lengthInPages": 3,
    "previousChapters": [],
    "mode": "single",
    "language": "pt-BR"
})

chapter1_text = chapter1_response.json()["text"]

# 2. Resumir Capítulo 1
summary_response = requests.post("http://localhost:8000/summarize", json={
    "chapterText": chapter1_text,
    "chapterTitle": "Capítulo 1",
    "language": "pt-BR"
})

summary = summary_response.json()

# 3. Gerar Capítulo 2 com contexto rico
chapter2_response = requests.post("http://localhost:8000/generate-chapter", json={
    "projectId": "test",
    "chapterId": "ch2",
    "projectTitle": "A Aventura",
    "chapterTitle": "Capítulo 2: Primeiros Passos",
    "chapterSummary": "Protagonista explora e encontra pistas",
    "previousChapters": [
        {
            "title": "Capítulo 1",
            "summary": summary["summary"],  # Resumo estruturado
            "generatedText": chapter1_text
        }
    ],
    "tone": "misterioso",
    "writingStyle": "narrativo",
    "setting": "floresta sombria",
    "lengthInPages": 3,
    "mode": "single",
    "language": "pt-BR"
})

print("✅ Capítulos gerados com continuidade perfeita!")
```

---

## �🔧 Configuração (.env)

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `GEMINI_API_KEY` | Chave da API (obrigatório) | - |
| `GEMINI_MODEL` | Modelo Gemini | `gemini-1.5-flash` |
| `TEMPERATURE` | Criatividade (0.0-1.0) | `0.7` |
| `MAX_OUTPUT_TOKENS` | Máximo de tokens | `8192` |
| `LOG_LEVEL` | Nível de log | `INFO` |
| `PORT` | Porta da API | `8000` |

---

## � Exemplo de Uso

```python
import requests

response = requests.post("http://localhost:8000/generate-chapter", json={
    "projectId": "test",
    "chapterId": "ch1",
    "projectTitle": "Teste",
    "chapterTitle": "Capítulo 1",
    "chapterSummary": "Início",
    # keyPoints é opcional
    "tone": "aventureiro",
    "writingStyle": "narrativo",
    "setting": "floresta",
    "lengthInPages": 2,
    "previousChapters": [],
    "mode": "single",
    "language": "pt-BR"
})

print(response.json()["text"])
```

---

## 🚀 Deploy (Render)

1. **Suba para GitHub:**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/SEU_USUARIO/taleseed-api.git
git push -u origin main
```

2. **Deploy no Render:**
   - Acesse https://render.com
   - "New +" → "Web Service"
   - Conecte seu repositório
   - Configure `GEMINI_API_KEY`
   - Deploy!

**URL:** `https://seu-app.onrender.com`

---

## 🏗️ Estrutura

```
.
├── main.py              # FastAPI app
├── requirements.txt     # Dependências
├── render.yaml          # Config Render
└── src/
    ├── models.py        # Modelos Pydantic
    └── services/
        └── ai_service.py # Serviço IA
```

---

## 📝 Licença

MIT

---

**Powered by Google Gemini AI** 🚀
│   ├── ARCHITECTURE.md    # Documentação técnica
│   ├── PROJECT_SUMMARY.md # Resumo da implementação
│   └── EXECUTIVE_SUMMARY.md # Resumo executivo
│
├── scripts/               # 🔧 Scripts auxiliares
│   ├── install.bat        # Instalação automática (Windows)
│   └── run.bat            # Execução facilitada (Windows)
│
├── library/               # 📚 Ebooks gerados
├── config/                # ⚙️ Configurações e planos
├── logs/                  # 📋 Logs de execução
│
├── main.py                # 🎯 Ponto de entrada
├── requirements.txt       # 📦 Dependências
├── .env                   # 🔑 Configurações (API key)
└── .env.example           # 📋 Template de configurações
```

---

## 📖 Documentação Completa

### 🎯 Para Começar
- **[Guia de Início Rápido](docs/QUICKSTART.md)** - Comece em 5 minutos
- **[Exemplo Prático](docs/EXAMPLE.md)** - Veja o agente em ação

### 📚 Documentação Detalhada
- **[Documentação Completa](docs/README.md)** - Tudo sobre o sistema
- **[Arquitetura](docs/ARCHITECTURE.md)** - Detalhes técnicos
- **[Resumo do Projeto](docs/PROJECT_SUMMARY.md)** - O que foi implementado
- **[Resumo Executivo](docs/EXECUTIVE_SUMMARY.md)** - Visão geral

---

## 💻 Uso

### Interface CLI

Execute `python main.py` e escolha uma opção:

```
╔═══════════════════════════════════════════════════════════════╗
║           📚  AGENTE GERADOR DE EBOOKS COM IA  📚            ║
╚═══════════════════════════════════════════════════════════════╝

MENU PRINCIPAL
1. 🆕 Criar novo projeto
2. ▶️  Retomar projeto existente
3. 📊 Ver status do projeto
4. 📁 Listar arquivos da biblioteca
5. 📖 Ler arquivo da biblioteca
6. 🔧 Configurações
7. ❌ Sair
```

### Exemplo de Prompt

```
Criar um ebook sobre "Introdução ao Machine Learning com Python"
com 10 capítulos cobrindo desde conceitos básicos até implementação
prática de modelos de classificação e regressão.

Público-alvo: Desenvolvedores Python iniciantes em ML
Tom: Didático e prático, com muitos exemplos de código
```

---

## ⚙️ Configuração

Edite o arquivo `.env` para personalizar:

```env
# Chave da API (OBRIGATÓRIO)
GEMINI_API_KEY=sua_chave_aqui

# Modelo Gemini
GEMINI_MODEL=gemini-1.5-pro

# Temperatura (0.0-1.0, maior = mais criativo)
TEMPERATURE=0.7

# Máximo de tokens de saída
MAX_OUTPUT_TOKENS=8192

# Pausa entre tarefas (segundos)
PAUSE_BETWEEN_TASKS=2
```

---

## 🎯 Casos de Uso

- 📚 **Autores**: Crie ebooks para vender
- 🎓 **Educadores**: Gere material didático
- 💼 **Empreendedores**: Produza guias e tutoriais
- 👨‍💻 **Desenvolvedores**: Documente projetos
- ✍️ **Escritores**: Crie rascunhos e outlines

---

## 📊 O Que Você Pode Criar

- **Ebooks completos** (10-50+ capítulos)
- **Artigos longos** e bem estruturados
- **Guias e tutoriais** passo a passo
- **Documentação técnica** profissional
- **Material educacional** didático

**Em 20-30 minutos → 40-100 páginas de conteúdo profissional!**

---

## 🛠️ Tecnologias

- **Python 3.8+**
- **Google Gemini API** (generativeai)
- **python-dotenv** (configurações)

---

## 📝 Requisitos

- Python 3.8 ou superior
- Chave da API do Google Gemini
- Conexão com internet

---

## 🚀 Scripts Auxiliares (Windows)

### Instalação Automática
```bash
scripts\install.bat
```

### Execução Facilitada
```bash
scripts\run.bat
```

---

## 🐛 Solução de Problemas

### Erro: "Chave da API não configurada"
- Verifique o arquivo `.env`
- Confirme que a chave está correta
- Use `.env.example` como referência

### Erro: "Falha ao gerar conteúdo"
- Verifique sua conexão
- Confirme que a API key é válida
- Consulte os logs em `logs/`

### Mais ajuda
Consulte a [documentação completa](docs/README.md)

---

## 📈 Performance Esperada

### Ebook Típico (10 capítulos)
- ⏱️ Tempo: 15-25 minutos
- 📝 Páginas: 30-50
- 🔢 Tokens: 60,000-100,000

---

## 🔐 Segurança

- ✅ API key em `.env` (não versionada)
- ✅ `.gitignore` configurado
- ✅ Logs não expõem dados sensíveis

---

## 🤝 Contribuindo

Sugestões e melhorias são bem-vindas!

---

## 📄 Licença

Este projeto é de código aberto para uso pessoal e educacional.

---

## 🎓 Como Funciona

1. **Planejamento**: Analisa seu prompt e cria plano de tarefas
2. **Execução**: Executa cada tarefa sequencialmente
3. **Contexto**: Mantém coerência entre todas as iterações
4. **Arquivos**: Salva resultados automaticamente
5. **Compilação**: Gera ebook final completo

---

## 💡 Dicas

1. **Seja específico** nos prompts
2. **Defina público-alvo** claramente
3. **Indique número de capítulos**
4. **Especifique tom e estilo**
5. **Revise sempre** o conteúdo gerado

---

## 📞 Links Úteis

- [📖 Documentação Completa](docs/README.md)
- [🚀 Início Rápido](docs/QUICKSTART.md)
- [💡 Exemplo Prático](docs/EXAMPLE.md)
- [🏗️ Arquitetura](docs/ARCHITECTURE.md)

---

## 🎉 Comece Agora!

```bash
# 1. Instale as dependências
python -m pip install -r requirements.txt

# 2. Execute o agente
python main.py

# 3. Escolha opção 1 e crie seu primeiro ebook!
```

---

**Desenvolvido com ❤️ usando Google Gemini API**

*Transforme ideias em ebooks completos em minutos!* 📚✨
