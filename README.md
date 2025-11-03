# 🌱 TaleSeed API

API REST para geração de conteúdo literário usando IA (Google Gemini).

## 📋 Visão Geral

O TaleSeed é uma API que permite gerar capítulos completos de livros e obter sugestões criativas (títulos, personagens, enredos, ambientações) usando inteligência artificial.

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- Chave de API do Google Gemini ([Obter aqui](https://makersuite.google.com/app/apikey))

### Passos

1. **Clone o repositório** (ou extraia os arquivos)

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Configure a chave da API:**

Crie um arquivo `.env` na raiz do projeto:
```env
GEMINI_API_KEY=sua_chave_aqui
GEMINI_MODEL=gemini-1.5-flash
LOG_LEVEL=INFO
TEMPERATURE=0.7
MAX_OUTPUT_TOKENS=8192
PORT=8000
```

4. **Execute a API:**
```bash
python main.py
```

A API estará disponível em `http://localhost:8000`

## 📡 Endpoints

### 1. Gerar Capítulo

**POST** `/generate-chapter`

Gera o texto completo de um capítulo baseado em resumo e contexto.

#### Request Body:
```json
{
  "projectId": "string",
  "chapterId": "string",
  "projectTitle": "A Jornada do Herói",
  "chapterTitle": "O Chamado à Aventura",
  "chapterSummary": "O protagonista recebe o chamado para sua jornada",
  "keyPoints": [
    "Introduzir o protagonista",
    "Apresentar o mentor",
    "Mostrar o mundo ordinário"
  ],
  "tone": "épico e inspirador",
  "writingStyle": "narrativo com diálogos",
  "setting": "Reino medieval fantástico",
  "lengthInPages": 8,
  "previousChapters": [
    {
      "title": "Prólogo",
      "summary": "Introdução ao mundo",
      "generatedText": "Texto do capítulo anterior (opcional)"
    }
  ],
  "mode": "single",
  "language": "pt-BR"
}
```

#### Response:
```json
{
  "text": "Era uma vez em um reino distante...",
  "tokensUsed": 2048,
  "metadata": {
    "model": "gemini-1.5-flash",
    "createdAt": "2025-11-03T10:30:00Z",
    "temperature": 0.7,
    "maxTokens": 8192
  }
}
```

### 2. Sugestões Criativas

**POST** `/creative-suggestions`

Gera sugestões criativas (títulos, nomes de personagens, enredos, ambientações).

#### Request Body:
```json
{
  "type": "title",
  "context": "Uma história sobre um jovem mago que descobre seus poderes",
  "genre": "fantasia",
  "tone": "épico e misterioso",
  "count": 5
}
```

**Tipos disponíveis:**
- `title` - Títulos para a história
- `character` - Nomes de personagens
- `plot` - Ideias de enredo
- `setting` - Ambientações

#### Response:
```json
{
  "suggestions": [
    {
      "text": "O Despertar dos Arcanos",
      "description": "Um título que evoca mistério e descoberta mágica"
    },
    {
      "text": "Sombras do Éter",
      "description": "Sugere um lado sombrio da magia"
    }
  ]
}
```

### 3. Health Check

**GET** `/health`

Verifica o status da API.

#### Response:
```json
{
  "status": "healthy",
  "service": "TaleSeed API"
}
```

## 📚 Documentação Interativa

Após iniciar a API, acesse:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

## 🔧 Configuração

### Variáveis de Ambiente (.env)

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `GEMINI_API_KEY` | Chave da API do Google Gemini | **Obrigatório** |
| `GEMINI_MODEL` | Modelo do Gemini a usar | `gemini-1.5-flash` |
| `LOG_LEVEL` | Nível de log (DEBUG/INFO/WARNING/ERROR) | `INFO` |
| `TEMPERATURE` | Criatividade (0.0-1.0) | `0.7` |
| `MAX_OUTPUT_TOKENS` | Máximo de tokens na resposta | `8192` |
| `PORT` | Porta da API | `8000` |

## 💡 Exemplos de Uso

### Python
```python
import requests

# Gerar um capítulo
response = requests.post("http://localhost:8000/generate-chapter", json={
    "projectId": "proj_001",
    "chapterId": "ch_001",
    "projectTitle": "Minha História",
    "chapterTitle": "Capítulo 1",
    "chapterSummary": "O início da aventura",
    "keyPoints": ["Apresentar protagonista", "Criar atmosfera"],
    "tone": "aventureiro",
    "writingStyle": "narrativo",
    "setting": "cidade moderna",
    "lengthInPages": 5,
    "previousChapters": [],
    "mode": "single",
    "language": "pt-BR"
})

print(response.json()["text"])
```

### cURL
```bash
curl -X POST "http://localhost:8000/creative-suggestions" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "character",
    "context": "Um detetive em uma cidade cyberpunk",
    "genre": "ficção científica noir",
    "tone": "sombrio",
    "count": 3
  }'
```

### JavaScript (Fetch)
```javascript
const response = await fetch('http://localhost:8000/generate-chapter', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    projectId: 'proj_001',
    chapterId: 'ch_001',
    projectTitle: 'Minha História',
    chapterTitle: 'Capítulo 1',
    chapterSummary: 'O início da aventura',
    keyPoints: ['Apresentar protagonista'],
    tone: 'aventureiro',
    writingStyle: 'narrativo',
    setting: 'cidade moderna',
    lengthInPages: 5,
    previousChapters: [],
    mode: 'single',
    language: 'pt-BR'
  })
});

const data = await response.json();
console.log(data.text);
```

## 🏗️ Estrutura do Projeto

```
.
├── main.py                      # Aplicação FastAPI principal
├── requirements.txt             # Dependências Python
├── .env                         # Configurações (não versionado)
├── README.md                    # Este arquivo
└── src/
    ├── __init__.py
    ├── models.py                # Modelos Pydantic
    └── services/
        ├── __init__.py
        └── ai_service.py        # Serviço de geração com IA
```

## 🔒 Segurança

- **Nunca** compartilhe sua `GEMINI_API_KEY`
- Em produção, configure CORS adequadamente
- Use HTTPS em produção
- Implemente rate limiting se necessário

## 🐛 Solução de Problemas

### Erro: "GEMINI_API_KEY não encontrada"
- Verifique se o arquivo `.env` existe na raiz do projeto
- Certifique-se de que a variável está definida corretamente

### Erro 500 ao gerar conteúdo
- Verifique sua conexão com a internet
- Confirme que sua chave API é válida
- Verifique os logs para mais detalhes

### API não inicia
- Verifique se a porta 8000 não está em uso
- Confirme que todas as dependências estão instaladas
- Execute: `pip install -r requirements.txt`

## 📝 Licença

Este projeto está sob a licença MIT.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se livre para abrir issues ou pull requests.

## 📧 Suporte

Para dúvidas ou suporte, abra uma issue no repositório do projeto.

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
