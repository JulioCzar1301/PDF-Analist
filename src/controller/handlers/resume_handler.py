"""
src/controller/handlers/resume_handler.py

Handler para geração de resumos com LLM.
"""

from typing import Any
from datetime import datetime
from .base_handler import BaseHandler
from src.llm import Summarizer


class ResumeHandler(BaseHandler):
    """
    Handler responsável pela geração de resumos usando LLM local.
    
    Funcionalidades:
    - Carregamento lazy do modelo LLM
    - Geração de resumos com Qwen 3B
    - Tratamento de textos grandes (Map-Reduce)
    - Gestão de memória e recursos
    """
    
    def __init__(self, view: Any, logger):
        """
        Inicializa o handler de resumo.
        
        Args:
            view: View para renderização de resultados.
            logger: Logger para registro de operações.
        """
        super().__init__(view, logger)
        self.summarizer = None
    
    
    def _ensure_summarizer(self, model: Any, tokenizer: Any) -> bool:
        """
        Garante que o summarizer está carregado (lazy loading).
        
        Args:
            model: Modelo LLM pré-carregado (ou None).
            tokenizer: Tokenizer pré-carregado (ou None).
        
        Returns:
            bool: True se o summarizer foi carregado com sucesso.
        """
        if self.summarizer is not None:
            return True
            
        try:
            self.logger.info("Carregando modelo LLM...")
            self.summarizer = Summarizer(model=model, tokenizer=tokenizer)
            self.logger.info("Modelo LLM carregado com sucesso")
            return True
            
        except MemoryError as e:
            self.logger.critical(f"Memória insuficiente para carregar modelo: {e}")
            self.view.render_error("Memória insuficiente para carregar o modelo LLM.")
            return False
        except OSError as e:
            self.logger.error(f"Erro de sistema ao carregar modelo: {e}")
            self.view.render_error(f"Erro de sistema ao carregar modelo: {e}")
            return False
        except Exception as e:
            self.logger.exception(f"Erro inesperado ao carregar modelo: {e}")
            self.view.render_error(f"Erro ao carregar modelo: {e}")
            return False
    
    
    def handle_resume(self, model: Any, llm_model: Any, tokenizer: Any) -> str:
        """
        Gera e renderiza um resumo do conteúdo do PDF.
        
        Args:
            model: Modelo PDFModel com os dados do documento.
            llm_model: Modelo LLM pré-carregado (ou None para carregar).
            tokenizer: Tokenizer pré-carregado (ou None para carregar).
        
        Returns:
            str: O resumo gerado pelo LLM (ou string vazia em caso de erro).
        """
        self.logger.info("Iniciando geração de resumo")
        
        # Extrair texto do PDF
        text = model.get_text()
        if not text:
            self.logger.error("Não foi possível extrair texto para resumo")
            self.view.render_error("Não foi possível extrair texto para resumo.")
            return ""

        self.logger.debug(f"Texto extraído: {len(text)} caracteres")

        # Carregar modelo LLM se necessário
        if not self._ensure_summarizer(llm_model, tokenizer):
            return ""

        # Gerar resumo
        try:
            self.logger.info("Gerando resumo com LLM...")
            start_time = datetime.now()
            
            resume = self.summarizer.summarize_text(text, max_output_tokens=2056)
            
            elapsed = (datetime.now() - start_time).total_seconds()
            self.logger.info(f"Resumo gerado com sucesso em {elapsed:.2f} segundos")
            self.logger.debug(f"Tamanho do resumo: {len(resume)} caracteres")
            
            self.view.render_success(f"Resumo do PDF:\n\n{resume}")
            return resume
            
        except MemoryError as e:
            self.logger.critical(f"Memória insuficiente durante geração: {e}")
            self.view.render_error("Memória insuficiente durante a geração do resumo.")
            return ""
        except RuntimeError as e:
            self.logger.error(f"Erro durante geração de resumo: {e}")
            self.view.render_error(str(e))
            return ""
        except Exception as e:
            self.logger.exception(f"Erro inesperado durante geração: {e}")
            self.view.render_error(f"Erro inesperado: {e}")
            return ""