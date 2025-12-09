"""
Models layer para análise de PDFs.

Contém toda a lógica de negócio (business logic) relacionada a PDFs.
Sem prints, sem I/O direto — apenas processamento e retorno de dados estruturados.
"""

from typing import Any, Dict, List, Optional, Tuple
import pymupdf
import os

from .extractor import extract_text_from_pdf
from .best_words import best_words_pdf
from .clean import clean
from .image import extract_images_from_pdf


class PDFModel:
    """Modelo responsável por operações de leitura e análise de PDF."""

    def __init__(self, pdf_path: str) -> None:
        """
        Inicializa o modelo com um caminho de PDF.

        Args:
            pdf_path: Caminho absoluto ou relativo ao arquivo PDF.
        """
        self.pdf_path: str = pdf_path
        self._validate_pdf()

    def _validate_pdf(self) -> None:
        """Valida se o arquivo PDF existe e é acessível."""
        if not os.path.exists(self.pdf_path):
            raise FileNotFoundError(f"PDF não encontrado: {self.pdf_path}")

    def get_page_count(self) -> int:
        """Retorna o número total de páginas."""
        try:
            doc = pymupdf.open(self.pdf_path)
            count = doc.page_count
            doc.close()
            return count
        except Exception as e:
            raise RuntimeError(f"Erro ao contar páginas: {e}")

    def get_word_count(self) -> int:
        """Retorna o número total de palavras no PDF."""
        try:
            text = extract_text_from_pdf(self.pdf_path)
            if text is None:
                return 0
            return len(text.split())
        except Exception as e:
            raise RuntimeError(f"Erro ao contar palavras: {e}")

    def get_file_size(self) -> int:
        """Retorna o tamanho do arquivo em bytes."""
        try:
            return os.path.getsize(self.pdf_path)
        except Exception as e:
            raise RuntimeError(f"Erro ao obter tamanho: {e}")

    def get_vocabulary_size(self) -> int:
        """Retorna o tamanho do vocabulário (palavras únicas)."""
        try:
            cleaned_text = clean(self.pdf_path)
            return len(set(cleaned_text.split()))
        except Exception as e:
            raise RuntimeError(f"Erro ao calcular vocabulário: {e}")

    def get_best_words(self, top_n: int = 10) -> List[Tuple[str, int]]:
        """
        Retorna as N palavras mais frequentes.

        Args:
            top_n: Número de palavras a retornar (padrão 10).

        Returns:
            Lista de tuplas (palavra, frequência).
        """
        try:
            result = best_words_pdf(self.pdf_path)
            if result is None:
                return []
            return result[:top_n]
        except Exception as e:
            raise RuntimeError(f"Erro ao analisar palavras: {e}")

    def get_text(self) -> Optional[str]:
        """Retorna o texto completo do PDF."""
        try:
            return extract_text_from_pdf(self.pdf_path)
        except Exception as e:
            raise RuntimeError(f"Erro ao extrair texto: {e}")

    def get_cleaned_text(self) -> str:
        """Retorna o texto limpo (sem stop words, pontuação)."""
        try:
            return clean(self.pdf_path)
        except Exception as e:
            raise RuntimeError(f"Erro ao limpar texto: {e}")

    def extract_images(self, output_dir: str, **kwargs: Any) -> Dict[str, Any]:
        """
        Extrai imagens do PDF para um diretório.

        Args:
            output_dir: Diretório de saída.
            **kwargs: Argumentos adicionais (dimlimit, relsize, abssize).

        Returns:
            Dicionário com resultado da extração.
        """
        try:
            return extract_images_from_pdf(self.pdf_path, output_dir, **kwargs)
        except Exception as e:
            raise RuntimeError(f"Erro ao extrair imagens: {e}")

    def get_summary(self) -> Dict[str, Any]:
        """
        Retorna um resumo completo de informações do PDF.

        Returns:
            Dicionário estruturado com informações do PDF.
        """
        try:
            return {
                "caminho": self.pdf_path,
                "numero_paginas": self.get_page_count(),
                "numero_palavras": self.get_word_count(),
                "tamanho_bytes": self.get_file_size(),
                "vocabulario": self.get_vocabulary_size(),
                "palavras_frequentes": self.get_best_words(),
            }
        except Exception as e:
            raise RuntimeError(f"Erro ao gerar resumo: {e}")
