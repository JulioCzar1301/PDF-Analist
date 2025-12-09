import pymupdf
from typing import Any, Dict, Optional
from .extractor import extract_text_from_pdf
from .best_words import best_words_pdf
from .clean import clean
import os
from .stop_words import STOP_WORDS


def info_pdf(pdf_path: Any) -> Optional[Dict[str, Any]]:
    """Retorna informações básicas sobre um arquivo PDF."""
    try:
        doc = pymupdf.open(pdf_path)

        return {
            "Número total de páginas": doc.page_count,
            "Número de palavras": len(extract_text_from_pdf(pdf_path).split()) ,
            "Tamanho do arquivo (em bytes)": os.path.getsize(pdf_path),
            "10 palavras mais frequentes": best_words_pdf(pdf_path),
            "Tamanho do vocabulário": len(set(clean(pdf_path).split())),

        }
    except Exception as e:
        print(f"Erro ao obter informações do PDF: {e}")
        return None