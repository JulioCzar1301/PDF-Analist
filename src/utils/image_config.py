"""
src/utils/image_config
"""
from dataclasses import dataclass

@dataclass
class ImageExtractionConfig:
    """Configuração para extração de imagens de PDFs."""
    dimlimit: int = 0  # Dimensão mínima (largura ou altura)
    relsize: float = 0.0  # Tamanho relativo mínimo
    abssize: int = 0  # Tamanho absoluto mínimo em bytes