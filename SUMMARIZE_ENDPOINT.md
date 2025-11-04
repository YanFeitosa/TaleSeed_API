# 📊 Endpoint `/summarize` - Resumo Focado em Continuidade

## 🎯 Propósito

O endpoint `/summarize` foi criado para resolver o problema de **continuidade entre capítulos**, gerando resumos **estruturados e ricos** que capturam todas as informações essenciais para manter coerência narrativa.

---

## 🆚 Por que não usar apenas o resumo manual?

### ❌ Resumo Manual Tradicional
```json
{
  "summary": "Protagonista acorda na floresta"
}
```

**Problemas:**
- Falta detalhes de personagens
- Não captura estado emocional final
- Omite locais específicos
- Perde eventos importantes

### ✅ Resumo Estruturado do `/summarize`
```json
{
  "summary": "João Silva acorda desorientado em uma clareira da Floresta Negra. Ele não se lembra de como chegou ali...",
  "characters": [
    "João Silva (protagonista, 35 anos, detetive)",
    "Voz misteriosa (entidade desconhecida)"
  ],
  "settings": [
    "Floresta Negra (clareira central)",
    "Ribeirão próximo à clareira"
  ],
  "keyEvents": [
    "João desperta sem memórias recentes",
    "Descobre ferimento na cabeça",
    "Ouve voz misteriosa entre árvores",
    "Decide seguir o som do ribeirão"
  ],
  "endingState": "João caminha em direção ao ribeirão, alerta e apreensivo. A voz misteriosa ainda ecoa em sua mente. Ele carrega uma sensação de que algo importante está prestes a ser revelado."
}
```

**Vantagens:**
- ✅ **Nomes completos** dos personagens
- ✅ **Locais específicos** com detalhes
- ✅ **Eventos ordenados** cronologicamente
- ✅ **Estado emocional final** detalhado
- ✅ **Tensão narrativa** preservada

---

## 📋 Estrutura da Response

### 1. `summary` (string)
**Resumo narrativo completo** em 3-5 parágrafos.

**O que inclui:**
- Eventos principais cronologicamente
- Ações e mudanças de estado
- Início e final do capítulo
- Tom e atmosfera

**Exemplo:**
```
"João Silva acorda em uma clareira da Floresta Negra, completamente desorientado. 
Não se lembra de como chegou ali, mas sente uma dor latejante na cabeça. 
Ao explorar o local, percebe pegadas recentes no solo úmido...

[continua com mais 2-3 parágrafos]"
```

---

### 2. `characters` (array de strings)
**Lista completa de personagens** mencionados no capítulo.

**Formato:** `"Nome completo (descrição/papel)"`

**Exemplos:**
```json
[
  "João Silva (protagonista, detetive particular, 35 anos)",
  "Maria Santos (testemunha, barista do Café Central)",
  "Voz misteriosa (entidade desconhecida)",
  "Inspector Carvalho (mencionado, não aparece)"
]
```

**Por que é importante:**
- Mantém consistência de nomes entre capítulos
- Evita personagens "esquecidos"
- Permite rastreamento de todos os envolvidos

---

### 3. `settings` (array de strings)
**Lista de locais/ambientações** do capítulo.

**Formato:** `"Nome do local (detalhes relevantes)"`

**Exemplos:**
```json
[
  "Floresta Negra (clareira central, densa vegetação)",
  "Ribeirão das Pedras (ao norte da clareira)",
  "Cabana abandonada (construção de madeira, teto parcialmente destruído)",
  "Café Central (mencionado em flashback)"
]
```

**Por que é importante:**
- Geografia consistente da história
- Evita erros de localização
- Permite construção de "mapa mental" da narrativa

---

### 4. `keyEvents` (array de strings)
**3-7 eventos mais importantes** do capítulo, em ordem cronológica.

**Exemplos:**
```json
[
  "João acorda desorientado na floresta",
  "Descobre ferimento na cabeça e pegadas no solo",
  "Ouve voz misteriosa entre as árvores",
  "Encontra cabana abandonada com sinais de luta",
  "Descobre foto rasgada de Maria Santos",
  "Decide seguir trilha que leva ao ribeirão"
]
```

**Por que é importante:**
- Timeline clara da narrativa
- Eventos que afetam próximos capítulos
- Base para continuidade de ações

---

### 5. `endingState` (string)
**O MAIS IMPORTANTE PARA CONTINUIDADE**

Descrição detalhada de **como o capítulo termina**.

**O que deve incluir:**
- Onde estão os personagens principais?
- Qual o estado físico/emocional deles?
- Qual a tensão/situação narrativa?
- O que está prestes a acontecer?

**Exemplo:**
```
"João está à beira do Ribeirão das Pedras, ainda segurando a foto rasgada de Maria. 
Está fisicamente exausto mas mentalmente alerta, com a voz misteriosa ainda ecoando 
em sua mente. Ele acabou de perceber que as pegadas que seguia levam diretamente 
para dentro da água. A sensação de perigo iminente se intensifica. Ele está prestes 
a decidir se cruza o ribeirão ou retorna à cabana."
```

**Por que é CRUCIAL:**
- Define ponto de partida do próximo capítulo
- Evita saltos temporais abruptos
- Mantém tensão e flow narrativo
- Preserva estado emocional

---

## 🔄 Como o `/summarize` Melhora a Continuidade

### Fluxo Tradicional (SEM /summarize)

```
Capítulo 1 gerado
    ↓
Resumo manual genérico: "João acorda na floresta"
    ↓
Capítulo 2 gerado (contexto pobre)
    ↓
❌ PROBLEMA: Capítulo 2 começa com João em local diferente
❌ Personagens secundários "desaparecem"
❌ Detalhes inconsistentes
```

### Fluxo Otimizado (COM /summarize)

```
Capítulo 1 gerado
    ↓
POST /summarize → Resumo rico e estruturado
    ↓
  - Personagens: João Silva, Maria Santos, Voz misteriosa
  - Locais: Floresta Negra, Ribeirão, Cabana
  - Estado final: João à beira do ribeirão, foto em mãos
    ↓
Capítulo 2 gerado (contexto RICO)
    ↓
✅ Capítulo 2 começa EXATAMENTE onde Cap 1 terminou
✅ João ainda está com a foto
✅ Ribeirão é mencionado corretamente
✅ Voz misteriosa continua presente
✅ CONTINUIDADE PERFEITA
```

---

## 💻 Exemplos de Uso

### Exemplo 1: Resumo Simples

**Request:**
```json
POST /summarize
{
  "chapterText": "João acordou com dor de cabeça. A floresta ao redor era densa e escura. Ele ouviu um ruído estranho vindo das árvores. Decidiu investigar e encontrou uma cabana abandonada...",
  "chapterTitle": "Capítulo 1: O Despertar",
  "language": "pt-BR"
}
```

**Response:**
```json
{
  "summary": "João acorda com forte dor de cabeça em uma floresta densa...",
  "characters": ["João (protagonista)"],
  "settings": ["Floresta densa e escura", "Cabana abandonada"],
  "keyEvents": [
    "João acorda com dor de cabeça",
    "Ouve ruído estranho",
    "Descobre cabana abandonada"
  ],
  "endingState": "João está em frente à cabana abandonada, curioso mas cauteloso...",
  "tokensUsed": 320
}
```

---

### Exemplo 2: Capítulo Complexo (múltiplos personagens)

**Request:**
```json
POST /summarize
{
  "chapterText": "[Capítulo longo com João, Maria, Inspector, 3 locais, múltiplos eventos]",
  "chapterTitle": "Capítulo 5: Revelações",
  "language": "pt-BR"
}
```

**Response:**
```json
{
  "summary": "João e Maria se encontram no Café Central para discutir as pistas...\n\nO Inspector Carvalho chega inesperadamente...\n\nA revelação sobre o passado de Maria muda tudo...",
  
  "characters": [
    "João Silva (protagonista, detetive particular)",
    "Maria Santos (testemunha chave, barista)",
    "Inspector Carvalho (polícia, antigo parceiro de João)",
    "Marcos (mencionado, suspeito principal)"
  ],
  
  "settings": [
    "Café Central (local do encontro)",
    "Delegacia do 5º distrito (mencionada)",
    "Apartamento de Maria (flashback)"
  ],
  
  "keyEvents": [
    "João e Maria se encontram no café",
    "Discussão sobre as pistas da cabana",
    "Inspector Carvalho revela nova informação",
    "Maria confessa segredo sobre seu passado",
    "João confronta o Inspector sobre omissões",
    "Decisão de investigar Marcos juntos"
  ],
  
  "endingState": "João, Maria e o Inspector estão no estacionamento do Café Central. A tensão entre João e Carvalho é palpável após a discussão acalorada. Maria está visivelmente abalada pela confissão que fez. Os três acabaram de concordar, relutantemente, em trabalhar juntos para localizar Marcos. João segura um envelope que o Inspector lhe entregou - ele ainda não o abriu. O sol está se pondo, e eles têm apenas algumas horas até o prazo que Marcos estabeleceu.",
  
  "tokensUsed": 580
}
```

---

## 🎯 Boas Práticas

### ✅ DO

1. **Use `/summarize` para TODOS os capítulos**
   - Mesmo que pareça "simples"
   - Informações estruturadas ajudam a IA

2. **Inclua `chapterTitle` sempre que possível**
   - Ajuda a IA contextualizar
   - Melhora qualidade do resumo

3. **Use o `summary` completo no `previousChapters`**
   - Não use apenas os primeiros parágrafos
   - O resumo já está otimizado

4. **Armazene todos os campos da response**
   - `characters`, `settings`, `keyEvents` podem ser úteis
   - Use para criar "wiki" do projeto

5. **Combine com texto completo em `generatedText`**
   ```json
   {
     "previousChapters": [
       {
         "title": "Cap 1",
         "summary": "[resumo do /summarize]",
         "generatedText": "[texto completo]"
       }
     ]
   }
   ```

### ❌ DON'T

1. **Não envie capítulos muito curtos (< 100 caracteres)**
   - Use `min_length=100` na validação
   - Texto insuficiente = resumo pobre

2. **Não ignore o `endingState`**
   - É a parte MAIS importante para continuidade
   - Use para começar o próximo capítulo

3. **Não edite manualmente o resumo gerado**
   - A IA otimizou para continuidade
   - Edições podem quebrar o fluxo

4. **Não use `/summarize` em textos que não são capítulos**
   - Otimizado para narrativa
   - Outros tipos de texto podem ter resultados ruins

---

## 🧪 Testando a Continuidade

### Checklist Pós-Geração

Após gerar Capítulo 2 usando resumo do `/summarize`:

- [ ] **Início conecta com final anterior?**
  - Cap 1 termina: "João à beira do ribeirão"
  - Cap 2 começa: "João observa a água corrente do ribeirão..."
  - ✅ Perfeito!

- [ ] **Personagens consistentes?**
  - Cap 1: "Maria Santos (barista)"
  - Cap 2: "Maria Santos aparece" (não "a barista Maria" ou "uma mulher chamada Maria")
  - ✅ Nome completo e consistente!

- [ ] **Locais consistentes?**
  - Cap 1: "Floresta Negra, Ribeirão das Pedras"
  - Cap 2: Continua nesses locais ou se move logicamente
  - ✅ Geografia consistente!

- [ ] **Estado emocional preservado?**
  - Cap 1 termina: João está "alerta e apreensivo"
  - Cap 2 começa: João continua cauteloso (não relaxado ou confiante repentinamente)
  - ✅ Emoções coerentes!

---

## 🔧 Troubleshooting

### Problema: "Resumo muito genérico"

**Causa:** Capítulo de entrada muito curto ou sem detalhes.

**Solução:**
- Gere capítulos com pelo menos 500 palavras
- Use `lengthInPages: 3` ou mais no `/generate-chapter`

---

### Problema: "Personagens não listados corretamente"

**Causa:** Nomes ambíguos ou não explícitos no texto.

**Solução:**
- Use nomes completos no capítulo gerado
- No prompt do `/generate-chapter`, especifique: "Use sempre nomes completos dos personagens"

---

### Problema: "`endingState` é muito curto"

**Causa:** Capítulo termina de forma abrupta.

**Solução:**
- No `/generate-chapter`, use `keyPoints` para guiar final:
  ```json
  {
    "keyPoints": [
      "...",
      "Capítulo deve terminar com João decidindo próxima ação"
    ]
  }
  ```

---

### Problema: "Continuidade ainda ruim mesmo usando `/summarize`"

**Possíveis Causas:**

1. **Não enviou `generatedText`:**
   ```json
   // ❌ Errado
   "previousChapters": [{"summary": "..."}]
   
   // ✅ Correto
   "previousChapters": [{
     "summary": "...",
     "generatedText": "[texto completo]"
   }]
   ```

2. **`chapterSummary` do novo capítulo é muito diferente:**
   - Deve ser continuação lógica do anterior
   - Evite saltos temporais grandes

3. **Tom/estilo mudaram:**
   - Mantenha mesmos valores de `tone` e `writingStyle`

---

## 📊 Performance e Custos

### Tokens Esperados

| Tamanho do Capítulo | Input Tokens | Output Tokens | Total |
|---------------------|--------------|---------------|-------|
| 500 palavras (~2 páginas) | ~600 | ~250 | ~850 |
| 1000 palavras (~4 páginas) | ~1200 | ~400 | ~1600 |
| 2000 palavras (~8 páginas) | ~2400 | ~600 | ~3000 |

### Tempo de Resposta

- Capítulo pequeno (500 palavras): **3-5 segundos**
- Capítulo médio (1000 palavras): **5-8 segundos**
- Capítulo grande (2000 palavras): **8-12 segundos**

### Custo (Google Gemini)

Com `gemini-1.5-flash` (preço aproximado):
- Capítulo médio: **$0.001 - $0.002** por resumo
- Muito econômico para a qualidade gerada!

---

## 🎓 Casos de Uso Avançados

### 1. Criar "Wiki" do Projeto

Acumule informações de todos os capítulos:

```python
all_characters = set()
all_settings = set()

for chapter in chapters:
    summary = summarize(chapter)
    all_characters.update(summary["characters"])
    all_settings.update(summary["settings"])

# Resultado: Base de conhecimento completa do projeto
```

---

### 2. Detectar Inconsistências

Compare personagens/locais entre capítulos:

```python
if "João Silva" in cap1_summary["characters"]:
    if "João" in cap2_summary["characters"] and "João Silva" not in cap2_summary["characters"]:
        print("⚠️ Aviso: Nome inconsistente!")
```

---

### 3. Gerar Timeline Automática

Use `keyEvents` de todos os capítulos:

```python
timeline = []
for i, chapter in enumerate(chapters):
    summary = summarize(chapter)
    for event in summary["keyEvents"]:
        timeline.append(f"Cap {i+1}: {event}")

# Timeline completa do livro!
```

---

## 📚 Recursos Relacionados

- **[CONTINUITY_FIX.md](CONTINUITY_FIX.md)** - Como o sistema de continuidade foi melhorado
- **[README.md](README.md)** - Documentação geral da API
- **[/generate-chapter](README.md#post-generate-chapter)** - Endpoint de geração de capítulos

---

## 🚀 Próximos Passos

1. **Teste o endpoint:**
   ```bash
   curl -X POST http://localhost:8000/summarize \
     -H "Content-Type: application/json" \
     -d '{"chapterText": "Seu capítulo aqui...", "language": "pt-BR"}'
   ```

2. **Integre no seu fluxo:**
   - Gere capítulo → Resuma → Use resumo no próximo

3. **Experimente:**
   - Teste com capítulos diferentes
   - Valide a qualidade da continuidade
   - Ajuste `lengthInPages` e `keyPoints` conforme necessário

---

**Criado:** 2025-11-03  
**Versão:** 1.0  
**Status:** ✅ Implementado e Documentado
