import pymupdf
from .stop_words import STOP_WORDS
from typing import Union


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
    
    except Exception as e:
        print(f"Erro ao limpar o texto: {e}")
        return ""
