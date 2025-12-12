"""
src/pdf/best_words.py

Este módulo fornece funcionalidades para extrair e analisar as palavras mais
frequentes em um arquivo PDF, retornando um ranking das palavras com maior
ocorrência no documento.
"""

from typing import List
from .clean import clean


def best_words_pdf(path: str) -> List[str]:
    """Retorna as palavras mais frequentes em um texto extraído de PDF."""
    try:
        text_cleaned = clean(path)
        words = text_cleaned.split()
        word_freq = {}

        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1

        sorted_words = sorted(word_freq.items(), key=lambda item: item[1], reverse=True)
        return sorted_words[:10]
    except FileNotFoundError as e:
        print(f"Arquivo PDF não encontrado: {e}")
        return None
    except ValueError as e:
        print(f"Erro ao processar o texto: {e}")
        return None
    except OSError as e:
        print(f"Erro ao acessar o arquivo: {e}")
        return None
