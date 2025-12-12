"""
Modulo de inicializacao do pacote CLI
"""
from typing import List
from .arguments import create_parser
from .views import ConsoleView

__all__: List[str] = ["create_parser","ConsoleView"]