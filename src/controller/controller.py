"""
src/controller/controller.py

Controller principal - Orquestra o fluxo MVC.
Delega operações específicas para handlers especializados.
"""

import os
import logging
from typing import Any
from src.cli.views import ConsoleView
from src.llm import Summarizer
from src.pdf import PDFModel
from .handlers import (
    InfoHandler,
    TextAnalysisHandler,
    ImageHandler,
    ResumeHandler,
    FinalResumeHandler
)


class Controller:
    """
    Controller responsável por orquestração MVC.
    
    Delega operações para handlers especializados mantendo
    o controller enxuto e focado em roteamento.
    """

    def __init__(self, view: Any = None, model: Any = None, tokenizer: Any = None) -> None:
        """
        Inicializa o controller e seus handlers.

        Args:
            view: View para renderização (padrão: ConsoleView).
            model: Modelo LLM pré-carregado (opcional).
            tokenizer: Tokenizer pré-carregado (opcional).
        """
        self.model = model
        self.tokenizer = tokenizer
        self.view = view or ConsoleView()
        self.summarizer = None
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Inicializar handlers especializados
        self.info_handler = InfoHandler(self.view, self.logger)
        self.text_handler = TextAnalysisHandler(self.view, self.logger)
        self.image_handler = ImageHandler(self.view, self.logger)
        self.resume_handler = ResumeHandler(self.view, self.logger)
        self.final_handler = FinalResumeHandler(self.view, self.logger)
        
        self.logger.info("=" * 80)
        self.logger.info("Controller inicializado")
        self.logger.info("=" * 80)


    def run(self, args: Any) -> None:
        """
        Orquestra a execução baseada em argumentos.

        Args:
            args: Argumentos do parser (contém path, info, best_words, etc).
        """
        try:
            self.logger.info(f"Iniciando processamento do arquivo: {args.path}")
            
            # Validar caminho do arquivo
            if not self._validate_file(args.path):
                return
            
            # Criar modelo PDF
            self.logger.debug(f"Criando PDFModel para: {args.path}")
            pdf_model = PDFModel(args.path)
            
            # Executar operação apropriada
            self._dispatch_operation(args, pdf_model)

        except FileNotFoundError as e:
            self._handle_error("Arquivo não encontrado", e)
        except MemoryError as e:
            self._handle_error("Erro de memória", e, critical=True)
        except (ModuleNotFoundError, ImportError) as e:
            self._handle_error("Erro de importação", e)
        except (ConnectionError, OSError) as e:
            self._handle_error("Erro de sistema", e)
        except ValueError as e:
            self._handle_error("Valor inválido", e)
        except RuntimeError as e:
            self._handle_error("Erro de execução", e)
        except KeyboardInterrupt:
            self.logger.warning("Operação interrompida pelo usuário")
            self.view.render_error("Operação interrompida pelo usuário.")
        except Exception as e:
            self.logger.exception(f"Erro inesperado: {e}")
            self.view.render_error(f"Erro inesperado: {e}")


    def _validate_file(self, path: str) -> bool:
        """Valida se o arquivo existe."""
        if not os.path.exists(path):
            self.logger.error(f"Arquivo não encontrado: {path}")
            self.view.render_error(f"Arquivo não encontrado: {path}")
            return False
        return True


    def _dispatch_operation(self, args: Any, pdf_model: PDFModel) -> None:
        """Roteia a operação para o handler apropriado."""
        
        # Mapeamento de argumentos para handlers
        dispatch_map = {
            "info": lambda: self.info_handler.handle_info(pdf_model),
            "best_words": lambda: self.text_handler.handle_best_words(pdf_model),
            "page_count": lambda: self.text_handler.handle_page_count(pdf_model),
            "words_count": lambda: self.text_handler.handle_word_count(pdf_model),
            "vocabulary_size": lambda: self.text_handler.handle_vocabulary_size(pdf_model),
            "headers": lambda: self.text_handler.handle_headers(pdf_model),
            "resume": lambda: self.resume_handler.handle_resume(
                pdf_model, self.model, self.tokenizer
            ),
            "extract_images": lambda: self.image_handler.handle_extract_images(
                pdf_model, args.output_dir, args.dimlimit, args.abssize, args.relsize
            ),
            "final_resume": lambda: self.final_handler.handle_final_resume(
                pdf_model, self.model, self.tokenizer
            ),
        }

        # Executar operação
        executed = False
        for arg_name, handler in dispatch_map.items():
            if getattr(args, arg_name, False):
                self.logger.info(f"Executando operação: {arg_name}")
                handler()
                executed = True
                self.logger.info(f"Operação '{arg_name}' concluída com sucesso")
                return

        if not executed:
            self.logger.warning("Nenhum argumento válido fornecido")
            self.view.render_error("Nenhum argumento válido fornecido.")


    def _handle_error(self, msg: str, error: Exception, critical: bool = False) -> None:
        """Centraliza tratamento de erros."""
        if critical:
            self.logger.critical(f"{msg}: {error}")
        else:
            self.logger.error(f"{msg}: {error}")
        self.view.render_error(f"{msg}: {error}")


    def start(self, args: Any) -> None:
        """Alias público para `run` — facilita uso externo."""
        self.run(args)