"""
Views layer para apresentação de dados.

Responsável por formatação e exibição de dados da camada de modelos.
Separa apresentação (console, JSON, HTML) da lógica de negócio.
"""

from typing import Any, Dict
import json
from abc import ABC, abstractmethod


class BaseView(ABC):
    """Classe base para todas as views."""

    @abstractmethod
    def render_info(self, data: Dict[str, Any]) -> None:
        """Renderiza informações gerais do PDF."""
        pass

    @abstractmethod
    def render_best_words(self, words: list) -> None:
        """Renderiza palavras mais frequentes."""
        pass

    @abstractmethod
    def render_error(self, message: str) -> None:
        """Renderiza mensagem de erro."""
        pass


class ConsoleView(BaseView):
    """View para exibição em console (terminal)."""

    def render_info(self, data: Dict[str, Any]) -> None:
        """
        Exibe informações do PDF formatadas em console.

        Args:
            data: Dicionário com informações do PDF.
        """
        print("\n" + "=" * 60)
        print("INFORMAÇÕES DO PDF".center(60))
        print("=" * 60)
        for key, value in data.items():
            if key == "palavras_frequentes":
                continue  # será renderizado separadamente
            print(f"{key.replace('_', ' ').title():<30} {value}")
        print("=" * 60 + "\n")

    def render_best_words(self, words: list) -> None:
        """
        Exibe palavras mais frequentes formatadas em console.

        Args:
            words: Lista de tuplas (palavra, frequência).
        """
        if not words:
            print("Nenhuma palavra frequente encontrada.")
            return

        print("\n" + "-" * 40)
        print("TOP 10 PALAVRAS MAIS FREQUENTES".center(40))
        print("-" * 40)
        for idx, (word, freq) in enumerate(words, 1):
            print(f"{idx:2d}. {word:<20} {freq:>5} ocorrências")
        print("-" * 40 + "\n")

    def render_error(self, message: str) -> None:
        """Exibe erro em console."""
        print(f"\n❌ ERRO: {message}\n")

    def render_page_count(self, count: int) -> None:
        """Exibe contagem de páginas."""
        print(f"\n📄 Número de páginas: {count}\n")

    def render_word_count(self, count: int) -> None:
        """Exibe contagem de palavras."""
        print(f"\n📝 Número de palavras: {count}\n")

    def render_vocabulary_size(self, size: int) -> None:
        """Exibe tamanho do vocabulário."""
        print(f"\n📚 Tamanho do vocabulário: {size} palavras únicas\n")

    def render_text_structure(self, text: str) -> None:
        """Exibe resumo da estrutura do texto."""
        lines = text.split('\n')
        paragraphs = [l for l in lines if l.strip()]
        print(f"\n📋 Estrutura do Texto:")
        print(f"   - Linhas: {len(lines)}")
        print(f"   - Parágrafos: {len(paragraphs)}")
        print(f"   - Caracteres: {len(text)}\n")

    def render_success(self, message: str) -> None:
        """Exibe mensagem de sucesso."""
        print(f"\n✅ {message}\n")


class JSONView(BaseView):
    """View para exibição em JSON (API/integração)."""

    def render_info(self, data: Dict[str, Any]) -> None:
        """Exibe informações em JSON."""
        print(json.dumps(data, indent=2, ensure_ascii=False))

    def render_best_words(self, words: list) -> None:
        """Exibe palavras mais frequentes em JSON."""
        output = {
            "palavras_frequentes": [
                {"posicao": idx, "palavra": word, "frequencia": freq}
                for idx, (word, freq) in enumerate(words, 1)
            ]
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))

    def render_error(self, message: str) -> None:
        """Exibe erro em JSON."""
        print(json.dumps({"erro": message}, indent=2, ensure_ascii=False))

    def render_page_count(self, count: int) -> None:
        """Exibe contagem de páginas em JSON."""
        print(json.dumps({"numero_paginas": count}))

    def render_word_count(self, count: int) -> None:
        """Exibe contagem de palavras em JSON."""
        print(json.dumps({"numero_palavras": count}))

    def render_vocabulary_size(self, size: int) -> None:
        """Exibe tamanho do vocabulário em JSON."""
        print(json.dumps({"vocabulario": size}))

    def render_success(self, message: str) -> None:
        """Exibe mensagem de sucesso em JSON."""
        print(json.dumps({"sucesso": message}))
