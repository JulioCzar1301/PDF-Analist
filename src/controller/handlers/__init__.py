"""
src/controller/handlers/__init__.py

Inicialização do pacote handlers.
Exporta todos os handlers para uso no controller.
"""

from .base_handler import BaseHandler
from .info_handler import InfoHandler
from .text_analysis_handler import TextAnalysisHandler
from .image_handler import ImageHandler
from .resume_handler import ResumeHandler
from .final_resume_handler import FinalResumeHandler

__all__ = [
    'BaseHandler',
    'InfoHandler',
    'TextAnalysisHandler',
    'ImageHandler',
    'ResumeHandler',
    'FinalResumeHandler',
]