import pymupdf 
from typing import Any, Optional


def extract_text_from_pdf(pdf_path: Any) -> Optional[str]:
    """Extrai texto de um arquivo PDF."""
    try:
        doc = pymupdf.open(pdf_path)
        text = ""
        
        for page in doc:
            text  += page.get_text()

        return text
    except Exception as e:
        print(f"Erro ao extrair texto: {e}")
        return None
