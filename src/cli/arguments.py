import argparse
from typing import Any


def create_parser() -> Any:

    parser = argparse.ArgumentParser(description="Exemplo simples com argparse")

    parser.add_argument("path", help="Passe a o caminho do arquivo pdf ou pasta")
    parser.add_argument("-info", help="Informações do PDF", action="store_true")
    parser.add_argument("-page_count", help="Número de páginas do PDF", action="store_true")
    parser.add_argument("-words_count", help="Contagem de palavras no PDF", action="store_true")
    parser.add_argument("-best_words", help="Palavras mais frequentes no PDF", action="store_true")
    parser.add_argument("-vocabulary_size", help="Tamanho do vocabulário do PDF", action="store_true")
    parser.add_argument("-text_structure", help="Estrutura do texto do PDF", action="store_true")
    parser.add_argument("-resume", help="Resumo do PDF", action="store_true")
    parser.add_argument("-extract_images", help="Extrair imagens do PDF", action="store_true")
    
    return parser.parse_args()

