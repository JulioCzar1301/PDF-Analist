"""
src/cli/arguments.py
Esse módulo define o parser de argumentos para a aplicação CLI.
"""

import argparse
from typing import Any


def create_parser() -> Any:
    """
    Cria e retorna o parser de argumentos da CLI.
    Args:
         None
    Returns:
        argparse.Namespace: Objeto contendo os argumentos parseados.
    """
    parser = argparse.ArgumentParser(description="Exemplo simples com argparse")

    parser.add_argument("path",
        help="Passe a o caminho do arquivo pdf")
    parser.add_argument("-info",
        help="Informações do PDF", 
        action="store_true")
    parser.add_argument("-page_count",
        help="Número de páginas do PDF", 
        action="store_true")
    parser.add_argument("-words_count",
        help="Contagem de palavras no PDF", 
        action="store_true")
    parser.add_argument("-best_words",
        help="Palavras mais frequentes no PDF", 
        action="store_true")
    parser.add_argument("-vocabulary_size",
        help="Tamanho do vocabulário do PDF", 
        action="store_true")
    parser.add_argument("-headers",
        help="Estrutura do texto do PDF", 
        action="store_true")
    parser.add_argument("-resume",
        help="Resumo do PDF", 
        action="store_true")
    parser.add_argument("-extract_images",
        help="Extrair imagens do PDF", 
        action="store_true")
    parser.add_argument("--output_dir",
        help="Diretório de saída para as imagens extraídas (padrão: ./extracted_images)",
        default="./extracted_images",
        type=str
    )
    parser.add_argument("--dimlimit",
        help="Dimensão mínima das imagens em pixels (largura ou altura)",
        type=int,
        default=50
    )
    parser.add_argument("--abssize",
        help="Tamanho mínimo do arquivo de imagem em bytes",
        type=int,
        default=1024
    )
    parser.add_argument("--relsize",
        help="Tamanho relativo mínimo",
        type=float,
        default=0.0
    )
    parser.add_argument("-final_resume",
        help="Emite o resumo fina com todas as informações",
        action="store_true"
    )
    return parser.parse_args()
