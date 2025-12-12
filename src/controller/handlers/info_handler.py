"""
src/controller/handlers/info_handler.py

Handler para informações gerais do PDF.
"""

from typing import Any
from .base_handler import BaseHandler


class InfoHandler(BaseHandler):
    """
    Handler responsável por exibir informações gerais do PDF.

    Inclui:
    - Número de páginas
    - Contagem de palavras
    - Tamanho do arquivo
    - Tamanho do vocabulário
    - Palavras mais frequentes
    """

    def handle_info(self, model: Any) -> None:
        """
        Renderiza informações completas do PDF.

        Args:
            model: Modelo PDFModel com os dados do documento.
        """
        try:
            self.logger.debug("Obtendo informações gerais do PDF")
            summary = model.get_summary()

            self.logger.info(f"PDF analisado: {summary['file']}")
            self.logger.info(f"Páginas: {summary['page_count']}, "
                           f"Palavras: {summary['word_count']}, "
                           f"Vocabulário: {summary['vocabulary']}")

            self.view.render_info(summary)
            self.view.render_best_words(summary["word_freq"])

        except RuntimeError as e:
            self.logger.error(f"Erro ao obter informações: {e}")
            self.view.render_error(str(e))