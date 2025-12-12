"""
src/controller/handlers/image_handler.py

Handler para extração de imagens do PDF.
"""

from typing import Any
from .base_handler import BaseHandler
from src.utils import ImageExtractionConfig


class ImageHandler(BaseHandler):
    """
    Handler responsável pela extração de imagens do PDF.

    Funcionalidades:
    - Extração de todas as imagens
    - Filtragem por dimensões mínimas
    - Filtragem por tamanho de arquivo
    - Salvamento em diretório customizável
    """

    def handle_extract_images(
        self,
        model: Any,
        output_dir: str,
        dimlimit: int,
        abssize: int,
        relsize: float
    ) -> None:
        """
        Extrai imagens do PDF com filtros configuráveis.

        Args:
            model: Modelo PDFModel com os dados do documento.
            output_dir: Diretório de saída para as imagens.
            dimlimit: Dimensão mínima (largura ou altura) em pixels.
            abssize: Tamanho mínimo do arquivo em bytes.
            relsize: Tamanho relativo mínimo.
        """
        try:
            self.logger.info("Iniciando extração de imagens")
            self.logger.debug(f"Parâmetros: dimlimit={dimlimit}, "
                            f"abssize={abssize}, relsize={relsize}")

            # Configurar filtros de extração
            config = ImageExtractionConfig(dimlimit, relsize, abssize)

            # Extrair imagens
            result = model.extract_images(output_dir, config)

            self.logger.info(f"Extração concluída: {result['extracted']}/{result['total']} imagens")
            self.logger.info(f"Imagens salvas em: {result['output_path']}")

            # Renderizar resultado
            self.view.render_success(
                f"Imagens extraídas com sucesso!\n"
                f"Total: {result['total']}\n"
                f"Extraídas: {result['extracted']}\n"
                f"Diretório: {result['output_path']}"
            )

        except RuntimeError as e:
            self.logger.error(f"Erro ao extrair imagens: {e}")
            self.view.render_error(str(e))
        except Exception as e:
            self.logger.exception(f"Erro inesperado na extração de imagens: {e}")
            self.view.render_error(f"Erro inesperado: {e}")