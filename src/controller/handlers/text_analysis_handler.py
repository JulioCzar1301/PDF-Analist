"""
src/controller/handlers/text_analysis_handler.py

Handler para análises de texto do PDF.
"""

from typing import Any
from .base_handler import BaseHandler


class TextAnalysisHandler(BaseHandler):
    """
    Handler responsável por análises textuais do PDF.
    
    Operações:
    - Palavras mais frequentes
    - Contagem de páginas
    - Contagem de palavras
    - Tamanho do vocabulário
    - Estrutura do documento (headers)
    """
    
    def handle_best_words(self, model: Any) -> None:
        """
        Renderiza as palavras mais frequentes do PDF.
        
        Args:
            model: Modelo PDFModel com os dados do documento.
        """
        try:
            self.logger.debug("Calculando palavras mais frequentes")
            words = model.get_best_words()
            
            self.logger.info(f"Top {len(words)} palavras mais frequentes extraídas")
            self.logger.debug(f"Palavras: {[w[0] for w in words[:5]]}")
            
            self.view.render_best_words(words)
            
        except RuntimeError as e:
            self.logger.error(f"Erro ao calcular palavras frequentes: {e}")
            self.view.render_error(str(e))

    
    def handle_page_count(self, model: Any) -> None:
        """
        Renderiza a contagem de páginas do PDF.
        
        Args:
            model: Modelo PDFModel com os dados do documento.
        """
        try:
            self.logger.debug("Obtendo contagem de páginas")
            count = model.get_page_count()
            
            self.logger.info(f"Total de páginas: {count}")
            self.view.render_page_count(count)
            
        except RuntimeError as e:
            self.logger.error(f"Erro ao contar páginas: {e}")
            self.view.render_error(str(e))

    
    def handle_word_count(self, model: Any) -> None:
        """
        Renderiza a contagem total de palavras do PDF.
        
        Args:
            model: Modelo PDFModel com os dados do documento.
        """
        try:
            self.logger.debug("Obtendo contagem de palavras")
            count = model.get_word_count()
            
            self.logger.info(f"Total de palavras: {count}")
            self.view.render_word_count(count)
            
        except RuntimeError as e:
            self.logger.error(f"Erro ao contar palavras: {e}")
            self.view.render_error(str(e))

    
    def handle_vocabulary_size(self, model: Any) -> None:
        """
        Renderiza o tamanho do vocabulário (palavras únicas).
        
        Args:
            model: Modelo PDFModel com os dados do documento.
        """
        try:
            self.logger.debug("Calculando tamanho do vocabulário")
            size = model.get_vocabulary_size()
            
            self.logger.info(f"Tamanho do vocabulário: {size} palavras únicas")
            self.view.render_vocabulary_size(size)
            
        except RuntimeError as e:
            self.logger.error(f"Erro ao calcular vocabulário: {e}")
            self.view.render_error(str(e))

    
    def handle_headers(self, model: Any) -> None:
        """
        Renderiza a estrutura do documento (títulos e seções).
        
        Args:
            model: Modelo PDFModel com os dados do documento.
        """
        try:
            self.logger.debug("Extraindo estrutura do texto")
            text = model.get_headers()
            
            if text:
                self.logger.info("Estrutura do texto extraída com sucesso")
                self.logger.debug(f"Tamanho da estrutura: {len(text)} caracteres")
                self.view.render_text_structure(text)
            else:
                self.logger.warning("Não foi possível extrair estrutura do texto")
                self.view.render_error("Não foi possível extrair texto.")
                
        except RuntimeError as e:
            self.logger.error(f"Erro ao extrair estrutura: {e}")
            self.view.render_error(str(e))