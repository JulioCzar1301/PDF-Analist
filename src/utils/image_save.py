"""
src/utils/image_config
"""

from typing import Any, Dict, Tuple, Union
from dataclasses import dataclass
from pathlib import Path

@dataclass
class ImageSaveContext:
    """Contexto para salvar uma imagem."""
    img: Tuple  # Tupla de imagem (xref, smask, width, height)
    doc: Any  # Documento PyMuPDF
    output_path: Path  # Caminho de saída
    page_num: int  # Número da página
    img_index: int  # Índice da imagem
    xreflist: list  # Lista de xrefs já processados