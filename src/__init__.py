"""
Módulo src - TaleSeed API.
"""

from .models import (
    GenerateChapterRequest,
    GenerateChapterResponse,
    CreativeSuggestionsRequest,
    CreativeSuggestionsResponse,
    PreviousChapter,
    GenerationMetadata,
    CreativeSuggestion
)
from .services.ai_service import AIService

__all__ = [
    'GenerateChapterRequest',
    'GenerateChapterResponse',
    'CreativeSuggestionsRequest',
    'CreativeSuggestionsResponse',
    'PreviousChapter',
    'GenerationMetadata',
    'CreativeSuggestion',
    'AIService',
]


__version__ = '1.0.0'
