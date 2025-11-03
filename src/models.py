"""
Modelos Pydantic para as APIs do TaleSeed.
"""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime


# ==================== Modelos para /generate-chapter ====================

class PreviousChapter(BaseModel):
    """Informações sobre capítulos anteriores."""
    title: str
    summary: str
    generatedText: Optional[str] = None


class GenerateChapterRequest(BaseModel):
    """Request para geração de capítulo."""
    projectId: str
    chapterId: str
    projectTitle: str
    chapterTitle: str
    chapterSummary: str
    keyPoints: Optional[List[str]] = Field(default_factory=list)
    tone: str
    writingStyle: str
    setting: str
    lengthInPages: int = Field(default=8, ge=1, le=50)
    previousChapters: List[PreviousChapter] = Field(default_factory=list)
    mode: Literal["single", "full"] = "single"
    language: str = "pt-BR"


class GenerationMetadata(BaseModel):
    """Metadados da geração."""
    model: str
    createdAt: datetime
    temperature: float
    maxTokens: int


class GenerateChapterResponse(BaseModel):
    """Response da geração de capítulo."""
    text: str
    tokensUsed: int
    metadata: GenerationMetadata


# ==================== Modelos para /creative-suggestions ====================

class CreativeSuggestion(BaseModel):
    """Uma sugestão criativa."""
    text: str
    description: Optional[str] = None


class CreativeSuggestionsRequest(BaseModel):
    """Request para sugestões criativas."""
    type: Literal["title", "character", "plot", "setting"]
    context: str
    genre: str
    tone: str
    count: int = Field(default=5, ge=1, le=20)


class CreativeSuggestionsResponse(BaseModel):
    """Response com sugestões criativas."""
    suggestions: List[CreativeSuggestion]
