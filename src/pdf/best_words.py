from typing import List, Dict
from .clean import clean
import pymupdf


def best_words_pdf(path: str) -> List[str]:
    """Retorna as palavras mais frequentes em um texto extraído de PDF."""
    try:
        doc = pymupdf.open(path)
        text_cleaned = clean(path)
        words = text_cleaned.split()
        word_freq = {}
        
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        sorted_words = sorted(word_freq.items(), key=lambda item: item[1], reverse=True)
        return sorted_words[:10]
    except Exception as e:
        print(f"Erro ao analisar palavras: {e}")
        return None

if __name__ == "__main__":
    path = "C:/Users/jc130/OneDrive/Área de Trabalho/Desafio_Python/public/arquivo_pdf/4-Vetebrados.pdf"
    result = best_words_pdf(path)
    print(result)