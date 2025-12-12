"""
src/pdf/clean.py

Este módulo fornece funcionalidades para extrair texto de arquivos PDF,
realizar limpeza (remoção de pontuações, normalização de caso) e filtrar
palavras irrelevantes (stop words) para preparar o texto para análise.
"""
from typing import Union
import pymupdf
from .stop_words import STOP_WORDS


def clean(path: Union[str, bytes]) -> str:
    """Limpa o texto extraído de um PDF, removendo pontuações e palavras irrelevantes."""
    try:
        doc = pymupdf.open(path)
        text_cleaned = ""
        for page in doc:
            text = page.get_text().lower()
            words = text.split()
            for word in words:
                word = word.strip('.,!?;"()[]{}')
                if word.isalpha() and word not in STOP_WORDS:
                    text_cleaned += word + " "
        return text_cleaned
    except ValueError as e:
        print(f"Erro ao processar o texto: {e}")
        return None
    except OSError as e:
        print(f"Erro ao acessar o arquivo: {e}")
        return None
