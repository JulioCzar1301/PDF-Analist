"""
src/pdf/extractor.py

Este módulo fornece funcionalidades para extrair texto bruto de arquivos PDF,
processando todas as páginas do documento e consolidando o conteúdo em uma
única string.
"""
from typing import Any, Optional
import pymupdf


def extract_text_from_pdf(pdf_path: Any) -> Optional[str]:
    """Extrai texto de um arquivo PDF."""
    try:
        doc = pymupdf.open(pdf_path)
        text = ""

        for page in doc:
            text  += page.get_text()

        return text
    except ValueError as e:
        print(f"Erro ao processar o texto: {e}")
        return None
    except OSError as e:
        print(f"Erro ao acessar o arquivo: {e}")
        return None
