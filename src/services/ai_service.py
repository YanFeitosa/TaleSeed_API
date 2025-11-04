"""
Serviço de IA para geração de conteúdo usando Gemini.
"""

import logging
from typing import List, Optional
from datetime import datetime
import google.generativeai as genai

from src.models import (
    GenerateChapterRequest,
    GenerateChapterResponse,
    GenerationMetadata,
    CreativeSuggestionsRequest,
    CreativeSuggestionsResponse,
    CreativeSuggestion
)

logger = logging.getLogger(__name__)


class AIService:
    """Serviço para geração de conteúdo com IA."""
    
    def __init__(
        self, 
        api_key: str, 
        model_name: str = "gemini-2.5-flash",
        temperature: float = 0.7,
        max_output_tokens: int = 8192
    ):
        """
        Inicializa o serviço de IA.
        
        Args:
            api_key: Chave da API do Google Gemini
            model_name: Nome do modelo a ser usado
            temperature: Temperatura para geração (0.0-1.0)
            max_output_tokens: Máximo de tokens na saída
        """
        self.model_name = model_name
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        
        genai.configure(api_key=api_key)
        
        self.generation_config = {
            "temperature": temperature,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": max_output_tokens,
        }
        
        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        
        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=self.generation_config,
            safety_settings=self.safety_settings
        )
        
        logger.info(f"AIService inicializado com modelo: {model_name}")
    
    def _build_chapter_prompt(self, request: GenerateChapterRequest) -> str:
        """Constrói o prompt para geração de capítulo."""
        
        # Se não há capítulos anteriores: é o PRIMEIRO capítulo (início do livro)
        if not request.previousChapters:
            return self._build_first_chapter_prompt(request)
        
        # Se há capítulos anteriores: continuação da história
        return self._build_continuation_chapter_prompt(request)
    
    def _build_first_chapter_prompt(self, request: GenerateChapterRequest) -> str:
        """Prompt especializado para o PRIMEIRO capítulo do livro."""
        
        # Pontos-chave (opcional)
        key_points_section = ""
        if request.keyPoints:
            key_points_text = "\n".join([f"- {point}" for point in request.keyPoints])
            key_points_section = f"\n## PONTOS-CHAVE A INCLUIR:\n{key_points_text}\n"
        
        prompt = f"""Você é um escritor profissional de ficção com décadas de experiência em criar aberturas memoráveis e envolventes.

## 📚 CONTEXTO DO PROJETO:
- **Título do Livro**: {request.projectTitle}
- **Idioma**: {request.language}

## 📖 CAPÍTULO A SER ESCRITO:
- **Título**: {request.chapterTitle}
- **Resumo**: {request.chapterSummary}

## 🎨 PARÂMETROS CRIATIVOS:
- **Tom**: {request.tone}
- **Estilo de Escrita**: {request.writingStyle}
- **Ambientação Principal**: {request.setting}
- **Extensão**: Aproximadamente {request.lengthInPages} páginas (cerca de {request.lengthInPages * 250} palavras)
{key_points_section}

## ⚠️ INSTRUÇÕES CRÍTICAS - PRIMEIRO CAPÍTULO:

### 🎯 Abertura Impactante
Este é o **PRIMEIRO CAPÍTULO** do livro. Você deve:

1. **GANCHAR O LEITOR nos primeiros parágrafos**
   - Comece com ação, diálogo intrigante, ou imagem vívida
   - Evite exposições longas ou descrições excessivas no início
   - Crie curiosidade imediata

2. **ESTABELEÇA a voz narrativa e o tom desde a primeira linha**
   - O tom deve ser {request.tone} desde o início
   - Mantenha consistência no estilo {request.writingStyle}

3. **APRESENTE personagens de forma orgânica**
   - Mostre, não conte (show, don't tell)
   - Revele características através de ações e diálogos
   - Use nomes completos na primeira menção

4. **CONSTRUA o mundo gradualmente**
   - Ambientação: {request.setting}
   - Integre detalhes sensoriais (sons, cheiros, texturas)
   - Não sobrecarregue com informação

5. **CRIE tensão ou conflito cedo**
   - Estabeleça stakes (o que está em jogo)
   - Plante questões que o leitor quer ver respondidas
   - Construa momentum narrativo

6. **ESTRUTURA recomendada**:
   - Primeiro terço: Gancho + apresentação do protagonista/cenário
   - Meio: Desenvolvimento da situação inicial
   - Final: Gancho para o próximo capítulo (cliffhanger leve ou promessa)

7. **QUALIDADE da prosa**:
   - Frases variadas (curtas e longas)
   - Diálogos naturais e reveladores de personalidade
   - Descrições vívidas mas econômicas
   - Ritmo adequado ao tom {request.tone}

8. **EXTENSÃO**: Escreva aproximadamente {request.lengthInPages * 250} palavras
   - Não seja nem muito breve nem prolixo demais
   - Cada parágrafo deve avançar a narrativa

## 📝 FORMATO DE SAÍDA:

Escreva APENAS o texto do capítulo, sem:
- ❌ Título do capítulo
- ❌ "Capítulo 1" ou numeração
- ❌ Prefácio ou introdução meta-textual
- ❌ Comentários sobre o texto
- ❌ Notas de autor

Apenas a narrativa pura em {request.language}.

---

**Comece agora a escrever o primeiro capítulo de "{request.projectTitle}":**"""

        return prompt
    
    def _build_continuation_chapter_prompt(self, request: GenerateChapterRequest) -> str:
        """Prompt especializado para capítulos de CONTINUAÇÃO."""
        
        # Contexto dos capítulos anteriores (otimizado)
        previous_context = "\n\n## 📚 CAPÍTULOS ANTERIORES (CONTEXTO ESSENCIAL):\n\n"
        previous_context += "⚠️ **ATENÇÃO**: Este capítulo deve continuar DIRETAMENTE da narrativa abaixo. Não ignore nada do que já foi estabelecido.\n\n"
        
        for idx, chapter in enumerate(request.previousChapters, 1):
            previous_context += f"### Capítulo {idx}: {chapter.title}\n\n"
            previous_context += f"**Resumo estruturado:**\n{chapter.summary}\n\n"
            
            if chapter.generatedText:
                # Extrai início e FIM (mais importante para continuidade)
                text = chapter.generatedText
                text_length = len(text)
                
                if text_length <= 2000:
                    # Capítulo curto: inclui tudo
                    previous_context += f"**Texto completo do capítulo:**\n{text}\n\n"
                else:
                    # Capítulo longo: primeiros 800 + últimos 1500 caracteres
                    beginning = text[:800]
                    ending = text[-1500:]
                    previous_context += f"**Início do capítulo:**\n{beginning}...\n\n"
                    previous_context += f"**🎯 FINAL DO CAPÍTULO (PONTO DE PARTIDA PARA CONTINUAÇÃO):**\n...{ending}\n\n"
            
            previous_context += "---\n\n"
        
        # Pontos-chave (opcional)
        key_points_section = ""
        if request.keyPoints:
            key_points_text = "\n".join([f"- {point}" for point in request.keyPoints])
            key_points_section = f"\n## 🎯 PONTOS-CHAVE A INCLUIR NESTE CAPÍTULO:\n{key_points_text}\n"
        
        prompt = f"""Você é um escritor profissional especializado em criar narrativas coesas com continuidade perfeita entre capítulos.

## 📚 CONTEXTO DO PROJETO:
- **Título do Livro**: {request.projectTitle}
- **Idioma**: {request.language}

## 📖 CAPÍTULO A SER ESCRITO (CONTINUAÇÃO):
- **Título**: {request.chapterTitle}
- **Resumo**: {request.chapterSummary}

## 🎨 PARÂMETROS CRIATIVOS:
- **Tom**: {request.tone}
- **Estilo de Escrita**: {request.writingStyle}
- **Ambientação Principal**: {request.setting}
- **Extensão**: Aproximadamente {request.lengthInPages} páginas (cerca de {request.lengthInPages * 250} palavras)
{key_points_section}{previous_context}

## ⚠️ INSTRUÇÕES CRÍTICAS - CAPÍTULO DE CONTINUAÇÃO:

### 🔗 CONTINUIDADE PERFEITA (PRIORIDADE MÁXIMA)

1. **COMECE exatamente onde o capítulo anterior terminou**
   - Analise cuidadosamente o FINAL do último capítulo (destacado acima)
   - O primeiro parágrafo DEVE conectar-se diretamente à última cena
   - Mantenha mesma linha temporal (sem saltos não explicados)
   - Preserve estado emocional e físico dos personagens

2. **CONSISTÊNCIA ABSOLUTA**
   - **Personagens**: Use sempre os mesmos nomes e características
   - **Locais**: Mantenha geografia e ambientações consistentes
   - **Eventos**: Não contradiga o que já aconteceu
   - **Tom e estilo**: Continue com tom {request.tone} e estilo {request.writingStyle}

3. **TRANSIÇÃO SUAVE**
   - Primeira frase deve ser ponte natural do capítulo anterior
   - Evite recapitulações longas ou repetitivas
   - Se mudar de cena/tempo, faça transição clara e justificada

4. **DESENVOLVIMENTO NARRATIVO**
   - Avance a trama de forma orgânica
   - Aprofunde personagens já estabelecidos
   - Introduza novos elementos com naturalidade
   - Mantenha ou aumente tensão/stakes

5. **DIÁLOGOS E AÇÕES**
   - Diálogos naturais e coerentes com personalidades estabelecidas
   - Ações que fazem sentido no contexto
   - Descrições sensoriais ricas mas econômicas

6. **RITMO E ESTRUTURA**
   - Início: Transição do capítulo anterior
   - Meio: Desenvolvimento de {request.chapterSummary}
   - Final: Gancho interessante para próximo capítulo

7. **QUALIDADE DA PROSA**
   - Variedade de estrutura de frases
   - Equilíbrio entre ação, diálogo e descrição
   - Prose vívida e envolvente
   - Ritmo adequado ao tom {request.tone}

8. **EXTENSÃO**: Aproximadamente {request.lengthInPages * 250} palavras
   - Desenvolva completamente as cenas
   - Não apresse nem prolongue desnecessariamente

### 🎯 CHECKLIST MENTAL ANTES DE ESCREVER:
- [ ] Li e entendi como o capítulo anterior terminou?
- [ ] Meu primeiro parágrafo conecta-se naturalmente ao final anterior?
- [ ] Estou mantendo nomes, locais e detalhes consistentes?
- [ ] O tom e estilo estão alinhados com o resto do livro?

## 📝 FORMATO DE SAÍDA:

Escreva APENAS o texto do capítulo, sem:
- ❌ Título ou numeração
- ❌ Recapitulação explícita ("No capítulo anterior...")
- ❌ Comentários meta-textuais
- ❌ Notas de rodapé

Apenas a narrativa pura e contínua em {request.language}.

---

**Continue a história de "{request.projectTitle}" agora:**"""

        return prompt
    
    def _build_creative_prompt(self, request: CreativeSuggestionsRequest) -> str:
        """Constrói o prompt aprimorado para sugestões criativas."""
        
        type_details = {
            "title": {
                "instruction": "títulos criativos e cativantes",
                "guidelines": """- Seja memorável e intrigante
- Evite clichês óbvios
- Capture a essência do gênero e tom
- Use linguagem evocativa
- Considere metáforas e simbolismo quando apropriado"""
            },
            "character": {
                "instruction": "nomes de personagens únicos e memoráveis",
                "guidelines": """- Considere origem cultural/étnica apropriada ao contexto
- Nome deve soar natural mas distintivo
- Reflita personalidade ou papel do personagem
- Evite nomes genéricos ou muito comuns
- Inclua possíveis apelidos quando relevante"""
            },
            "plot": {
                "instruction": "ideias de enredo originais e envolventes",
                "guidelines": """- Apresente conflito claro e interessante
- Inclua gancho emocional ou intelectual
- Considere arcos narrativos completos
- Pense em stakes (o que está em jogo)
- Sugira potencial para desenvolvimento"""
            },
            "setting": {
                "instruction": "ambientações ricas e imersivas",
                "guidelines": """- Descreva elementos sensoriais (visual, som, cheiro)
- Considere aspectos culturais e sociais
- Pense em como o local afeta a história
- Inclua detalhes únicos e memoráveis
- Sugira atmosfera e mood"""
            }
        }
        
        details = type_details.get(request.type, {
            "instruction": "sugestões criativas",
            "guidelines": "- Seja criativo e original"
        })
        
        prompt = f"""Você é um consultor criativo de elite especializado em desenvolvimento de histórias e narrativas.

## 📖 CONTEXTO DO PROJETO:
{request.context}

## 🎨 PARÂMETROS CRIATIVOS:
- **Gênero**: {request.genre}
- **Tom desejado**: {request.tone}
- **Tipo de sugestão**: {request.type}

## 🎯 SUA TAREFA:
Gere {request.count} {details["instruction"]} que sejam:
- **Originais** e não-clichês
- **Apropriados** para o gênero {request.genre}
- **Alinhados** com o tom {request.tone}
- **Bem desenvolvidos** com contexto suficiente

## 📋 DIRETRIZES ESPECÍFICAS:
{details["guidelines"]}

## 📝 FORMATO DE RESPOSTA (OBRIGATÓRIO):

Para cada sugestão, use este formato exato:

[SUGESTÃO 1]
Texto: [Sua sugestão principal aqui]
Descrição: [Explicação breve de 1-2 frases sobre por que esta sugestão funciona ou detalhes adicionais relevantes]

[SUGESTÃO 2]
Texto: [Sua sugestão principal aqui]
Descrição: [Explicação breve]

... (continue até {request.count} sugestões)

## ⚠️ IMPORTANTE:
- Seja CRIATIVO e ORIGINAL - evite o óbvio
- Mantenha coerência com gênero {request.genre} e tom {request.tone}
- Cada sugestão deve ser única e distinta das outras
- Descrições devem agregar valor real

---

**Gere {request.count} sugestões agora:**"""

        return prompt
    
    def _parse_creative_suggestions(self, text: str, count: int) -> List[CreativeSuggestion]:
        """Parseia o texto gerado em sugestões estruturadas."""
        suggestions = []
        
        # Divide por [SUGESTÃO X]
        parts = text.split("[SUGESTÃO")
        
        for part in parts[1:]:  # Pula a primeira parte vazia
            if len(suggestions) >= count:
                break
                
            lines = part.strip().split("\n")
            suggestion_text = ""
            description = ""
            
            for line in lines:
                line = line.strip()
                if line.startswith("Texto:"):
                    suggestion_text = line.replace("Texto:", "").strip()
                elif line.startswith("Descrição:"):
                    description = line.replace("Descrição:", "").strip()
            
            if suggestion_text:
                suggestions.append(CreativeSuggestion(
                    text=suggestion_text,
                    description=description if description else None
                ))
        
        # Se não conseguiu parsear corretamente, tenta uma abordagem mais simples
        if len(suggestions) < count and "\n" in text:
            suggestions = []
            lines = [l.strip() for l in text.split("\n") if l.strip()]
            for line in lines[:count]:
                # Remove numeração se houver
                clean_line = line.lstrip("0123456789.-) ")
                if clean_line:
                    suggestions.append(CreativeSuggestion(
                        text=clean_line,
                        description=None
                    ))
        
        return suggestions
    
    async def generate_chapter(self, request: GenerateChapterRequest) -> GenerateChapterResponse:
        """
        Gera um capítulo completo.
        
        Args:
            request: Dados da requisição
            
        Returns:
            Response com o texto gerado e metadados
        """
        logger.info(f"Gerando capítulo: {request.chapterTitle}")
        
        prompt = self._build_chapter_prompt(request)
        
        try:
            response = self.model.generate_content(prompt)
            
            if not response.text:
                raise ValueError("Resposta vazia da API")
            
            # Calcula tokens usados (aproximado)
            tokens_used = len(response.text.split())
            
            metadata = GenerationMetadata(
                model=self.model_name,
                createdAt=datetime.utcnow(),
                temperature=self.temperature,
                maxTokens=self.max_output_tokens
            )
            
            logger.info(f"Capítulo gerado com sucesso. Tokens: {tokens_used}")
            
            return GenerateChapterResponse(
                text=response.text,
                tokensUsed=tokens_used,
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"Erro ao gerar capítulo: {e}")
            raise
    
    async def generate_creative_suggestions(
        self, 
        request: CreativeSuggestionsRequest
    ) -> CreativeSuggestionsResponse:
        """
        Gera sugestões criativas.
        
        Args:
            request: Dados da requisição
            
        Returns:
            Response com as sugestões
        """
        logger.info(f"Gerando sugestões criativas do tipo: {request.type}")
        
        prompt = self._build_creative_prompt(request)
        
        try:
            response = self.model.generate_content(prompt)
            
            if not response.text:
                raise ValueError("Resposta vazia da API")
            
            suggestions = self._parse_creative_suggestions(response.text, request.count)
            
            # Garante que temos o número de sugestões pedido
            if len(suggestions) < request.count:
                logger.warning(f"Gerado apenas {len(suggestions)} de {request.count} sugestões")
            
            logger.info(f"Sugestões criativas geradas: {len(suggestions)}")
            
            return CreativeSuggestionsResponse(suggestions=suggestions)
            
        except Exception as e:
            logger.error(f"Erro ao gerar sugestões criativas: {e}")
            raise
    
    async def summarize_chapter(
        self, 
        request
    ):
        """
        Gera resumo completo de capítulo focado em continuidade narrativa.
        
        Args:
            request: SummarizeRequest com o texto do capítulo
            
        Returns:
            SummarizeResponse com resumo estruturado em campo único
        """
        logger.info(f"Gerando resumo de capítulo focado em continuidade")
        
        prompt = self._build_summarize_prompt(request)
        
        try:
            response = self.model.generate_content(prompt)
            
            if not response.text:
                raise ValueError("Resposta vazia da API")
            
            # Usa o texto completo como resumo estruturado
            summary_text = response.text.strip()
            
            # Calcula tokens usados (aproximado)
            tokens_used = len(response.text.split())
            
            logger.info(f"Resumo gerado com sucesso. Tokens: {tokens_used}")
            
            from src.models import SummarizeResponse
            return SummarizeResponse(
                summary=summary_text,
                tokensUsed=tokens_used
            )
            
        except Exception as e:
            logger.error(f"Erro ao gerar resumo: {e}")
            raise
    
    def _build_summarize_prompt(self, request) -> str:
        """Constrói prompt para resumo focado em continuidade."""
        
        title_context = f"\n**Título do Capítulo:** {request.chapterTitle}\n" if request.chapterTitle else ""
        
        prompt = f"""Você é um assistente especializado em análise literária e continuidade narrativa.

Sua tarefa é criar um resumo ESTRUTURADO do capítulo abaixo, focando em informações essenciais para manter CONTINUIDADE narrativa em capítulos futuros.
{title_context}
## TEXTO DO CAPÍTULO:
{request.chapterText}

---

## INSTRUÇÕES:

Analise o texto e extraia:

1. **RESUMO NARRATIVO** (3-5 parágrafos):
   - Resuma os eventos principais de forma cronológica
   - Foque em AÇÕES e MUDANÇAS de estado
   - Destaque o INÍCIO e o FINAL do capítulo (crucial para continuidade)
   - Mantenha tom objetivo mas capte a essência da narrativa

2. **PERSONAGENS** (lista):
   - Liste TODOS os personagens mencionados
   - Inclua nome completo e breve descrição/papel
   - Exemplo: "João Silva (protagonista, detetive)", "Maria (testemunha)"

3. **AMBIENTAÇÕES** (lista):
   - Liste TODOS os locais/cenários mencionados
   - Seja específico: "Café Central da cidade", não apenas "café"
   - Inclua detalhes relevantes: "Floresta escura ao norte da vila"

4. **EVENTOS-CHAVE** (lista ordenada):
   - Liste os 3-7 eventos mais importantes do capítulo
   - Em ordem cronológica
   - Foque em eventos que afetam a trama

5. **ESTADO FINAL** (1-2 parágrafos):
   - Como o capítulo TERMINA? (CRUCIAL para próximo capítulo)
   - Onde estão os personagens principais?
   - Qual o estado emocional/físico deles?
   - Qual a situação/tensão narrativa ao final?
   - O que está prestes a acontecer?

---

## FORMATO DE RESPOSTA (use exatamente este formato):

[RESUMO]
(Seu resumo narrativo aqui em 3-5 parágrafos)

[PERSONAGENS]
- Nome 1 (descrição/papel)
- Nome 2 (descrição/papel)
- Nome 3 (descrição/papel)

[AMBIENTAÇÕES]
- Local 1 (detalhes)
- Local 2 (detalhes)

[EVENTOS-CHAVE]
1. Primeiro evento importante
2. Segundo evento importante
3. Terceiro evento importante

[ESTADO FINAL]
(Descrição detalhada de como o capítulo termina - 1-2 parágrafos)

---

Responda em {request.language}. Seja PRECISO e DETALHADO - essas informações serão usadas para manter continuidade perfeita no próximo capítulo."""

        return prompt
    
    def _parse_summary_response(self, response_text: str) -> dict:
        """Parse da resposta estruturada do resumo."""
        
        result = {
            "summary": "",
            "characters": [],
            "settings": [],
            "keyEvents": [],
            "endingState": ""
        }
        
        try:
            # Remove espaços extras
            text = response_text.strip()
            
            # Extrai seções usando marcadores
            import re
            
            # RESUMO
            resumo_match = re.search(r'\[RESUMO\](.*?)\[PERSONAGENS\]', text, re.DOTALL | re.IGNORECASE)
            if resumo_match:
                result["summary"] = resumo_match.group(1).strip()
            
            # PERSONAGENS
            personagens_match = re.search(r'\[PERSONAGENS\](.*?)\[AMBIENTAÇÕES\]', text, re.DOTALL | re.IGNORECASE)
            if personagens_match:
                chars_text = personagens_match.group(1).strip()
                # Extrai linhas que começam com - ou número
                chars = re.findall(r'^[-•*]\s*(.+?)$', chars_text, re.MULTILINE)
                result["characters"] = [c.strip() for c in chars if c.strip()]
            
            # AMBIENTAÇÕES
            ambientacoes_match = re.search(r'\[AMBIENTAÇÕES\](.*?)\[EVENTOS-CHAVE\]', text, re.DOTALL | re.IGNORECASE)
            if ambientacoes_match:
                settings_text = ambientacoes_match.group(1).strip()
                settings = re.findall(r'^[-•*]\s*(.+?)$', settings_text, re.MULTILINE)
                result["settings"] = [s.strip() for s in settings if s.strip()]
            
            # EVENTOS-CHAVE
            eventos_match = re.search(r'\[EVENTOS-CHAVE\](.*?)\[ESTADO FINAL\]', text, re.DOTALL | re.IGNORECASE)
            if eventos_match:
                events_text = eventos_match.group(1).strip()
                # Extrai linhas numeradas ou com marcadores
                events = re.findall(r'^(?:\d+\.|-|•|\*)\s*(.+?)$', events_text, re.MULTILINE)
                result["keyEvents"] = [e.strip() for e in events if e.strip()]
            
            # ESTADO FINAL
            estado_match = re.search(r'\[ESTADO FINAL\](.*?)$', text, re.DOTALL | re.IGNORECASE)
            if estado_match:
                result["endingState"] = estado_match.group(1).strip()
            
            # Validações básicas
            if not result["summary"]:
                result["summary"] = "Resumo não disponível"
            if not result["endingState"]:
                result["endingState"] = "Estado final não especificado"
                
        except Exception as e:
            logger.error(f"Erro ao fazer parse do resumo: {e}")
            # Fallback: usa texto completo como resumo
            result["summary"] = response_text
            result["endingState"] = "Erro ao processar estado final"
        
        return result
