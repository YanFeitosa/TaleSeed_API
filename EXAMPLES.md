# 🧪 Exemplos de Teste da TaleSeed API

Exemplos práticos para testar os endpoints da API.

## 📝 Pré-requisitos

1. API rodando: `python main.py`
2. Variáveis configuradas no `.env`

---

## 1️⃣ Teste: Health Check

Verifica se a API está online.

### cURL
```bash
curl http://localhost:8000/health
```

### Python
```python
import requests

response = requests.get("http://localhost:8000/health")
print(response.json())
```

**Resposta Esperada:**
```json
{
  "status": "healthy",
  "service": "TaleSeed API"
}
```

---

## 2️⃣ Teste: Gerar Capítulo Simples

### cURL
```bash
curl -X POST "http://localhost:8000/generate-chapter" ^
  -H "Content-Type: application/json" ^
  -d "{\"projectId\":\"proj_001\",\"chapterId\":\"ch_001\",\"projectTitle\":\"A Viagem Perdida\",\"chapterTitle\":\"Capítulo 1: O Início\",\"chapterSummary\":\"João descobre um mapa antigo em seu sótão\",\"keyPoints\":[\"Apresentar João\",\"Encontrar o mapa\",\"Despertar curiosidade\"],\"tone\":\"misterioso\",\"writingStyle\":\"narrativo\",\"setting\":\"Casa antiga\",\"lengthInPages\":3,\"previousChapters\":[],\"mode\":\"single\",\"language\":\"pt-BR\"}"
```

### Python
```python
import requests
import json

url = "http://localhost:8000/generate-chapter"
data = {
    "projectId": "proj_001",
    "chapterId": "ch_001",
    "projectTitle": "A Viagem Perdida",
    "chapterTitle": "Capítulo 1: O Início",
    "chapterSummary": "João descobre um mapa antigo em seu sótão",
    "keyPoints": [
        "Apresentar João",
        "Encontrar o mapa",
        "Despertar curiosidade"
    ],
    "tone": "misterioso",
    "writingStyle": "narrativo",
    "setting": "Casa antiga",
    "lengthInPages": 3,
    "previousChapters": [],
    "mode": "single",
    "language": "pt-BR"
}

response = requests.post(url, json=data)
result = response.json()

print("=" * 60)
print("CAPÍTULO GERADO")
print("=" * 60)
print(result["text"])
print("\n" + "=" * 60)
print(f"Tokens usados: {result['tokensUsed']}")
print(f"Modelo: {result['metadata']['model']}")
print("=" * 60)
```

### JavaScript
```javascript
const url = "http://localhost:8000/generate-chapter";
const data = {
  projectId: "proj_001",
  chapterId: "ch_001",
  projectTitle: "A Viagem Perdida",
  chapterTitle: "Capítulo 1: O Início",
  chapterSummary: "João descobre um mapa antigo em seu sótão",
  keyPoints: [
    "Apresentar João",
    "Encontrar o mapa",
    "Despertar curiosidade"
  ],
  tone: "misterioso",
  writingStyle: "narrativo",
  setting: "Casa antiga",
  lengthInPages: 3,
  previousChapters: [],
  mode: "single",
  language: "pt-BR"
};

fetch(url, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(data)
})
.then(res => res.json())
.then(result => {
  console.log("CAPÍTULO GERADO");
  console.log("=".repeat(60));
  console.log(result.text);
  console.log("\nTokens usados:", result.tokensUsed);
  console.log("Modelo:", result.metadata.model);
});
```

---

## 3️⃣ Teste: Gerar Capítulo com Contexto

Gera um segundo capítulo usando o primeiro como contexto.

### Python
```python
import requests

url = "http://localhost:8000/generate-chapter"
data = {
    "projectId": "proj_001",
    "chapterId": "ch_002",
    "projectTitle": "A Viagem Perdida",
    "chapterTitle": "Capítulo 2: Desvendando o Mapa",
    "chapterSummary": "João analisa o mapa e percebe que ele leva a um tesouro escondido",
    "keyPoints": [
        "Decifrar o mapa",
        "Descobrir a localização",
        "Decidir ir atrás do tesouro"
    ],
    "tone": "aventureiro e empolgante",
    "writingStyle": "narrativo com diálogos",
    "setting": "Biblioteca da cidade",
    "lengthInPages": 4,
    "previousChapters": [
        {
            "title": "Capítulo 1: O Início",
            "summary": "João descobre um mapa antigo em seu sótão",
            "generatedText": "João subiu ao sótão pela primeira vez em anos..."
        }
    ],
    "mode": "single",
    "language": "pt-BR"
}

response = requests.post(url, json=data)
result = response.json()

print(result["text"])
```

---

## 4️⃣ Teste: Sugestões de Títulos

### cURL
```bash
curl -X POST "http://localhost:8000/creative-suggestions" ^
  -H "Content-Type: application/json" ^
  -d "{\"type\":\"title\",\"context\":\"Uma história sobre uma jovem que descobre poderes mágicos\",\"genre\":\"fantasia jovem adulto\",\"tone\":\"inspirador e mágico\",\"count\":5}"
```

### Python
```python
import requests

url = "http://localhost:8000/creative-suggestions"
data = {
    "type": "title",
    "context": "Uma história sobre uma jovem que descobre poderes mágicos",
    "genre": "fantasia jovem adulto",
    "tone": "inspirador e mágico",
    "count": 5
}

response = requests.post(url, json=data)
result = response.json()

print("SUGESTÕES DE TÍTULOS:")
print("=" * 60)
for i, suggestion in enumerate(result["suggestions"], 1):
    print(f"\n{i}. {suggestion['text']}")
    if suggestion.get('description'):
        print(f"   → {suggestion['description']}")
```

---

## 5️⃣ Teste: Sugestões de Personagens

### Python
```python
import requests

url = "http://localhost:8000/creative-suggestions"
data = {
    "type": "character",
    "context": "Um thriller psicológico em uma mansão isolada",
    "genre": "suspense",
    "tone": "sombrio e tenso",
    "count": 4
}

response = requests.post(url, json=data)
result = response.json()

print("SUGESTÕES DE PERSONAGENS:")
print("=" * 60)
for suggestion in result["suggestions"]:
    print(f"\n• {suggestion['text']}")
    if suggestion.get('description'):
        print(f"  {suggestion['description']}")
```

---

## 6️⃣ Teste: Sugestões de Enredo

### Python
```python
import requests

url = "http://localhost:8000/creative-suggestions"
data = {
    "type": "plot",
    "context": "Ficção científica em um futuro distópico",
    "genre": "ficção científica distópica",
    "tone": "crítico e reflexivo",
    "count": 3
}

response = requests.post(url, json=data)
result = response.json()

print("SUGESTÕES DE ENREDO:")
print("=" * 60)
for i, suggestion in enumerate(result["suggestions"], 1):
    print(f"\n{i}. {suggestion['text']}")
    if suggestion.get('description'):
        print(f"   {suggestion['description']}")
```

---

## 7️⃣ Teste: Sugestões de Ambientação

### Python
```python
import requests

url = "http://localhost:8000/creative-suggestions"
data = {
    "type": "setting",
    "context": "Romance histórico no século XIX",
    "genre": "romance histórico",
    "tone": "romântico e nostálgico",
    "count": 4
}

response = requests.post(url, json=data)
result = response.json()

print("SUGESTÕES DE AMBIENTAÇÃO:")
print("=" * 60)
for suggestion in result["suggestions"]:
    print(f"\n📍 {suggestion['text']}")
    if suggestion.get('description'):
        print(f"   {suggestion['description']}")
```

---

## 🔄 Script de Teste Completo

Teste todos os endpoints de uma vez:

```python
import requests
import time

BASE_URL = "http://localhost:8000"

def test_health():
    print("\n" + "="*60)
    print("🏥 TESTE 1: Health Check")
    print("="*60)
    response = requests.get(f"{BASE_URL}/health")
    print(response.json())
    return response.status_code == 200

def test_generate_chapter():
    print("\n" + "="*60)
    print("📖 TESTE 2: Gerar Capítulo")
    print("="*60)
    data = {
        "projectId": "test_001",
        "chapterId": "ch_001",
        "projectTitle": "Teste API",
        "chapterTitle": "Capítulo de Teste",
        "chapterSummary": "Um teste rápido",
        "keyPoints": ["Testar API", "Verificar resposta"],
        "tone": "neutro",
        "writingStyle": "narrativo",
        "setting": "Sala de testes",
        "lengthInPages": 1,
        "previousChapters": [],
        "mode": "single",
        "language": "pt-BR"
    }
    response = requests.post(f"{BASE_URL}/generate-chapter", json=data)
    result = response.json()
    print(f"Texto gerado: {result['text'][:100]}...")
    print(f"Tokens: {result['tokensUsed']}")
    return response.status_code == 200

def test_creative_suggestions():
    print("\n" + "="*60)
    print("💡 TESTE 3: Sugestões Criativas")
    print("="*60)
    data = {
        "type": "title",
        "context": "Uma história de teste",
        "genre": "teste",
        "tone": "neutro",
        "count": 3
    }
    response = requests.post(f"{BASE_URL}/creative-suggestions", json=data)
    result = response.json()
    print(f"Sugestões geradas: {len(result['suggestions'])}")
    for s in result['suggestions']:
        print(f"  • {s['text']}")
    return response.status_code == 200

def run_all_tests():
    print("\n" + "🧪 INICIANDO TESTES DA TALESEED API")
    print("="*60)
    
    results = []
    
    # Teste 1
    try:
        results.append(("Health Check", test_health()))
        time.sleep(1)
    except Exception as e:
        print(f"❌ Erro: {e}")
        results.append(("Health Check", False))
    
    # Teste 2
    try:
        results.append(("Gerar Capítulo", test_generate_chapter()))
        time.sleep(2)
    except Exception as e:
        print(f"❌ Erro: {e}")
        results.append(("Gerar Capítulo", False))
    
    # Teste 3
    try:
        results.append(("Sugestões Criativas", test_creative_suggestions()))
    except Exception as e:
        print(f"❌ Erro: {e}")
        results.append(("Sugestões Criativas", False))
    
    # Resumo
    print("\n" + "="*60)
    print("📊 RESUMO DOS TESTES")
    print("="*60)
    for test_name, passed in results:
        status = "✅ PASSOU" if passed else "❌ FALHOU"
        print(f"{test_name}: {status}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    print(f"\nTotal: {passed}/{total} testes passaram")

if __name__ == "__main__":
    run_all_tests()
```

---

## 📚 Documentação Interativa

Acesse a documentação interativa (Swagger UI):
```
http://localhost:8000/docs
```

Ou ReDoc:
```
http://localhost:8000/redoc
```

---

## ⚠️ Notas

- Os tempos de resposta podem variar (geralmente 5-30 segundos para geração de capítulos)
- O campo `generatedText` em `previousChapters` é opcional
- Para capítulos maiores, aumente `lengthInPages` (1 página ≈ 250 palavras)
- O parsing de sugestões criativas pode variar - a API tenta extrair o melhor formato possível
