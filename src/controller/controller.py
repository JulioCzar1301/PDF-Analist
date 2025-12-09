from typing import Any
from src.pdf.models import PDFModel
from src.cli.views import ConsoleView


class Controller:
    """
    Controller responsável por orquestração MVC.
    
    - Recebe requisições (args) do usuário
    - Usa PDFModel para processar dados (business logic)
    - Usa ConsoleView para exibir resultados (presentation)
    - Não contém lógica de negócio ou apresentação direta
    """

    def __init__(self, view: Any = None) -> None:
        """
        Inicializa o controller.

        Args:
            view: View para renderização (padrão: ConsoleView).
        """
        self.view = view or ConsoleView()

    def run(self, args: Any) -> None:
        """
        Orquestra a execução baseada em argumentos.

        Args:
            args: Argumentos do parser (contém path, info, best_words, etc).
        """
        try:
            # Instancia o modelo com o caminho do PDF
            pdf_model = PDFModel(args.path)

            # Despacha para a ação apropriada
            if args.info:
                self._handle_info(pdf_model)
            elif args.best_words:
                self._handle_best_words(pdf_model)
            elif args.page_count:
                self._handle_page_count(pdf_model)
            elif args.words_count:
                self._handle_word_count(pdf_model)
            elif args.vocabulary_size:
                self._handle_vocabulary_size(pdf_model)
            elif args.text_structure:
                self._handle_text_structure(pdf_model)
            elif args.resume:
                self._handle_resume(pdf_model)
            elif args.extract_images:
                self._handle_extract_images(pdf_model)
            else:
                self.view.render_error("Nenhum argumento válido fornecido.")
        except FileNotFoundError as e:
            self.view.render_error(str(e))
        except RuntimeError as e:
            self.view.render_error(str(e))
        except Exception as e:
            self.view.render_error(f"Erro inesperado: {str(e)}")

    def _handle_info(self, model: PDFModel) -> None:
        """Renderiza informações completas do PDF."""
        summary = model.get_summary()
        self.view.render_info(summary)
        self.view.render_best_words(summary["palavras_frequentes"])

    def _handle_best_words(self, model: PDFModel) -> None:
        """Renderiza palavras mais frequentes."""
        words = model.get_best_words()
        self.view.render_best_words(words)

    def _handle_page_count(self, model: PDFModel) -> None:
        """Renderiza contagem de páginas."""
        count = model.get_page_count()
        self.view.render_page_count(count)

    def _handle_word_count(self, model: PDFModel) -> None:
        """Renderiza contagem de palavras."""
        count = model.get_word_count()
        self.view.render_word_count(count)

    def _handle_vocabulary_size(self, model: PDFModel) -> None:
        """Renderiza tamanho do vocabulário."""
        size = model.get_vocabulary_size()
        self.view.render_vocabulary_size(size)

    def _handle_text_structure(self, model: PDFModel) -> None:
        """Renderiza análise da estrutura do texto."""
        text = model.get_text()
        if text:
            self.view.render_text_structure(text)
        else:
            self.view.render_error("Não foi possível extrair texto.")

    def _handle_resume(self, model: PDFModel) -> None:
        """Renderiza um resumo do conteúdo."""
        # Este é um placeholder para integração com summarizer (LLM)
        text = model.get_text()
        if text:
            # TODO: Integrar com modelo de summarização (ex: LLM)
            self.view.render_success(f"Resumo do PDF (primeiros 500 chars):\n\n{text[:500]}...")
        else:
            self.view.render_error("Não foi possível extrair texto para resumo.")

    def _handle_extract_images(self, model: PDFModel) -> None:
        """Renderiza resultado da extração de imagens."""
        import os
        output_dir = os.path.join(os.path.dirname(model.pdf_path), "extracted_images")
        result = model.extract_images(output_dir)
        self.view.render_success(
            f"Imagens extraídas com sucesso!\n"
            f"Total: {result['total']}\n"
            f"Extraídas: {result['extracted']}\n"
            f"Diretório: {result['output_path']}"
        )
     
