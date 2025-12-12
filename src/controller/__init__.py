"""
src/controller/__init__.py

Inicialização do pacote controller.

"""

from .controller import Controller
from .logger_config import setup_logging

__all__ = [
    'Controller',
    'setup_logging'
]