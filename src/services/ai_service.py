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
        
        # Contexto dos capítulos anteriores
        previous_context = ""
        if request.previousChapters:
            previous_context = "\n\n## CAPÍTULOS ANTERIORES:\n"
            for idx, chapter in enumerate(request.previousChapters, 1):
                previous_context += f"\n### Capítulo {idx}: {chapter.title}\n"
                previous_context += f"Resumo: {chapter.summary}\n"
                if chapter.generatedText:
                    # Usa apenas os primeiros 500 caracteres para não sobrecarregar
                    text_preview = chapter.generatedText[:500] + "..." if len(chapter.generatedText) > 500 else chapter.generatedText
                    previous_context += f"Trecho: {text_preview}\n"
        
        # Pontos-chave
        key_points_text = "\n".join([f"- {point}" for point in request.keyPoints])
        
        prompt = f"""Você é um escritor profissional especializado em criar narrativas envolventes.

## INFORMAÇÕES DO PROJETO:
- Título do Projeto: {request.projectTitle}
- Idioma: {request.language}

## CAPÍTULO A SER ESCRITO:
- Título: {request.chapterTitle}
- Resumo: {request.chapterSummary}

## PARÂMETROS DE ESCRITA:
- Tom: {request.tone}
- Estilo: {request.writingStyle}
- Ambientação: {request.setting}
- Extensão desejada: Aproximadamente {request.lengthInPages} páginas (cerca de {request.lengthInPages * 250} palavras)

## PONTOS-CHAVE A INCLUIR:
{key_points_text}
{previous_context}

## INSTRUÇÕES:
1. Escreva o capítulo completo em {request.language}
2. Mantenha o tom {request.tone} e o estilo {request.writingStyle}
3. Certifique-se de incluir todos os pontos-chave mencionados
4. A narrativa deve fluir naturalmente dos capítulos anteriores (se houver)
5. Use diálogos, descrições vívidas e desenvolvimento de personagens
6. Crie uma narrativa envolvente que prenda a atenção do leitor
7. O capítulo deve ter cerca de {request.lengthInPages * 250} palavras

Escreva APENAS o texto do capítulo, sem títulos, prefácio ou comentários adicionais."""

        return prompt
    
    def _build_creative_prompt(self, request: CreativeSuggestionsRequest) -> str:
        """Constrói o prompt para sugestões criativas."""
        
        type_instructions = {
            "title": "títulos criativos e cativantes para a história",
            "character": "nomes de personagens únicos e memoráveis",
            "plot": "ideias de enredo interessantes e originais",
            "setting": "ambientações ricas e detalhadas"
        }
        
        instruction = type_instructions.get(request.type, "sugestões criativas")
        
        prompt = f"""Você é um consultor criativo especializado em escrita criativa.

## CONTEXTO:
{request.context}

## PARÂMETROS:
- Gênero: {request.genre}
- Tom: {request.tone}

## TAREFA:
Gere {request.count} {instruction}.

## FORMATO DE RESPOSTA:
Para cada sugestão, forneça:
1. O texto principal da sugestão
2. Uma breve descrição explicativa (1-2 frases)

Formato:
[SUGESTÃO 1]
Texto: [texto aqui]
Descrição: [descrição aqui]

[SUGESTÃO 2]
...

Seja criativo, original e alinhado com o gênero {request.genre} e tom {request.tone}."""

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
