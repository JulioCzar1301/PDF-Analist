"""
src/controller/handlers.py

Handlers especializados para cada tipo de operação.
Cada handler é responsável por uma categoria específica de operações.
"""

import logging
from typing import Any

class BaseHandler:
    """Handler base com funcionalidades comuns."""

    def __init__(self, view: Any, logger: logging.Logger):
        self.view = view
        self.logger = logger


