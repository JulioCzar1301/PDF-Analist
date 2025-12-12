"""
Main entry point for PDF analysis application.

Este mnodulo inicia o logging, o CLI e o Controller
"""

from src.cli import create_parser
from src.controller import Controller
from src.controller import setup_logging

def main():
    """Execução e controle do sistema"""

    setup_logging()

    args = create_parser()
    controller = Controller()
    controller.run(args)


if __name__ == "__main__":
    main()
