"""
TaleSeed API - API para geração de conteúdo literário usando IA.
"""

import logging
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from src.models import (
    GenerateChapterRequest,
    GenerateChapterResponse,
    CreativeSuggestionsRequest,
    CreativeSuggestionsResponse
)
from src.services.ai_service import AIService


# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação."""
    # Startup
    logger.info("Iniciando TaleSeed API...")
    
    # Carrega variáveis de ambiente
    project_dir = Path(__file__).parent
    load_dotenv(project_dir / ".env")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY não configurada!")
        raise ValueError("GEMINI_API_KEY não encontrada no arquivo .env")
    
    # Lê todas as configurações do .env
    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    temperature = float(os.getenv("TEMPERATURE", "0.7"))
    max_tokens = int(os.getenv("MAX_OUTPUT_TOKENS", "8192"))
    log_level = os.getenv("LOG_LEVEL", "INFO")
    
    # Configura nível de log conforme .env
    logging.getLogger().setLevel(getattr(logging, log_level.upper()))
    
    logger.info(f"Configurações carregadas do .env:")
    logger.info(f"  - Modelo: {model_name}")
    logger.info(f"  - Temperatura: {temperature}")
    logger.info(f"  - Max Tokens: {max_tokens}")
    logger.info(f"  - Log Level: {log_level}")
    
    app.state.ai_service = AIService(
        api_key=api_key,
        model_name=model_name,
        temperature=temperature,
        max_output_tokens=max_tokens
    )
    
    logger.info("TaleSeed API inicializada com sucesso!")
    
    yield
    
    # Shutdown
    logger.info("Encerrando TaleSeed API...")


# Cria aplicação FastAPI
app = FastAPI(
    title="TaleSeed API",
    description="API para geração de conteúdo literário usando IA",
    version="2.0.0",
    lifespan=lifespan
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Endpoint raiz."""
    return {
        "name": "TaleSeed API",
        "version": "2.0.0",
        "status": "online"
    }


@app.get("/health")
async def health_check():
    """Verifica o status da API."""
    return {
        "status": "healthy",
        "service": "TaleSeed API"
    }


@app.post(
    "/generate-chapter",
    response_model=GenerateChapterResponse,
    status_code=status.HTTP_200_OK,
    tags=["Generation"]
)
async def generate_chapter(request: GenerateChapterRequest):
    """
    Gera o texto completo de um capítulo baseado em resumo e contexto.
    
    Este endpoint recebe informações sobre um capítulo (título, resumo, pontos-chave, etc.)
    e gera o texto completo usando IA, respeitando o tom, estilo e configurações fornecidas.
    """
    try:
        ai_service: AIService = app.state.ai_service
        response = await ai_service.generate_chapter(request)
        return response
    
    except ValueError as e:
        logger.error(f"Erro de validação: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    except Exception as e:
        logger.error(f"Erro ao gerar capítulo: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao gerar capítulo. Por favor, tente novamente."
        )


@app.post(
    "/creative-suggestions",
    response_model=CreativeSuggestionsResponse,
    status_code=status.HTTP_200_OK,
    tags=["Generation"]
)
async def creative_suggestions(request: CreativeSuggestionsRequest):
    """
    Gera sugestões criativas (títulos, nomes de personagens, enredos, ambientações).
    
    Este endpoint recebe o tipo de sugestão desejada e o contexto, e retorna
    uma lista de sugestões criativas geradas pela IA.
    """
    try:
        ai_service: AIService = app.state.ai_service
        response = await ai_service.generate_creative_suggestions(request)
        return response
    
    except ValueError as e:
        logger.error(f"Erro de validação: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    except Exception as e:
        logger.error(f"Erro ao gerar sugestões criativas: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao gerar sugestões. Por favor, tente novamente."
        )


if __name__ == "__main__":
    import uvicorn
    
    # Carrega porta do .env ou usa 8000 como padrão
    port = int(os.getenv("PORT", "8000"))
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
