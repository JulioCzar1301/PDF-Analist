"""
Extração de imagens de documentos PDF com tratamento de casos especiais.

Este módulo fornece funcionalidades para extrair imagens de arquivos PDF,
incluindo tratamento de transparências (/SMask) e espaços de cor customizados.

Baseado no exemplo oficial do PyMuPDF:
    https://github.com/pymupdf/PyMuPDF-Utilities/blob/master/examples/extract-images/extract-from-pages.py

Adaptações:
    - Removida dependência do PySimpleGUI
    - Adicionado suporte a Path do pathlib
    - Melhorias na nomenclatura de arquivos
    - Documentação expandida

Referências:
    McKie, J. X. (2018). extract-from-pages.py. PyMuPDF-Utilities.
    https://github.com/pymupdf/PyMuPDF-Utilities

Licença Original:
    GNU GPL V3
    Copyright (c) 2018 Jorj X. McKie

Requisitos:
    - PyMuPDF >= 1.18.18

Data:
    2025-12-05
"""

from pathlib import Path
from typing import Any, Dict, Tuple, Union
import pymupdf
from src.utils import ImageExtractionConfig, ImageSaveContext


def recoverpix(doc: Any, item: Tuple) -> Dict[str, Union[str, int, bytes]]:
    """
    Recupera imagem tratando casos especiais:
    - Imagens com /SMask (soft mask/transparência)
    - Imagens com /ColorSpace especial
    """
    xref = item[0]  # xref da imagem no PDF
    smask = item[1]  # xref do /SMask (se existir)

    # Caso especial: imagem tem /SMask ou /Mask (transparência)
    if smask > 0:
        pix0 = pymupdf.Pixmap(doc.extract_image(xref)["image"])
        if pix0.alpha:  # remove canal alpha se já existir
            pix0 = pymupdf.Pixmap(pix0, 0)
        mask = pymupdf.Pixmap(doc.extract_image(smask)["image"])

        try:
            pix = pymupdf.Pixmap(pix0, mask)
        except (RuntimeError, ValueError, OSError):
            pix = pymupdf.Pixmap(doc.extract_image(xref)["image"])

        if pix0.n > 3:
            ext = "pam"
        else:
            ext = "png"

        return {
            "ext": ext,
            "colorspace": pix.colorspace.n,
            "image": pix.tobytes(ext),
        }

    # Caso especial: /ColorSpace customizado
    # Converte para RGB PNG para garantir compatibilidade
    if "/ColorSpace" in doc.xref_object(xref, compressed=True):
        pix = pymupdf.Pixmap(doc, xref)
        pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
        return {
            "ext": "png",
            "colorspace": 3,
            "image": pix.tobytes("png"),
        }

    # Caso padrão: extração direta
    return doc.extract_image(xref)


def _should_extract_image(img: Tuple,
                          xreflist: list,
                          config: ImageExtractionConfig,
                          doc: Any) -> bool:
    """Verifica se uma imagem deve ser extraída baseado nos filtros."""
    xref = img[0]
    width = img[2]
    height = img[3]

    # Verificar se já extraímos esta imagem
    if xref in xreflist:
        return False

    # Filtro: dimensão mínima
    if min(width, height) <= config.dimlimit:
        print(f"  → Imagem {xref} muito pequena ({width}x{height})")
        return False

    # Recuperar imagem para obter tamanho
    image = recoverpix(doc, img)
    imgdata = image["image"]
    n = image["colorspace"]

    # Filtro: tamanho absoluto mínimo
    if len(imgdata) <= config.abssize:
        print(f"  → Imagem {xref} arquivo muito pequeno ({len(imgdata)} bytes)")
        return False

    # Filtro: tamanho relativo (densidade)
    if width * height * n > 0:  # evitar divisão por zero
        if len(imgdata) / (width * height * n) <= config.relsize:
            print(f"  → Imagem {xref} densidade muito baixa")
            return False

    return True


def extract_images_from_pdf(
    pdf_path: Union[str, Path],
    output_dir: Union[str, Path],
    config: ImageExtractionConfig = None,
) -> Dict[str, Union[int, str, None]]:
    """
    Extrai imagens de um arquivo PDF com filtros opcionais.

    Parâmetros:
    -----------
    pdf_path : str
        Caminho do arquivo PDF
    output_dir : str
        Diretório de saída
    config : ImageExtractionConfig, optional
        Configuração de filtros de extração. Usa valores padrão se None.

    Exemplo:
        config = ImageExtractionConfig(dimlimit=100, abssize=2048, relsize=0.05)
        extract_images_from_pdf("doc.pdf", "output/", config)
    """
    if config is None:
        config = ImageExtractionConfig()

    try:
        # Preparar caminho base (sem criar a pasta ainda)
        output_path = Path(output_dir) / Path(pdf_path).stem
        folder_created = False
        
        # Abrir PDF e processar
        doc = pymupdf.open(str(pdf_path))
        xreflist = []
        stats = {"total": 0, "extracted": 0, "output_path": None}

        for page_num, page in enumerate(doc):
            image_list = page.get_images(full=True)
            stats["total"] += len(image_list)

            for img_index, img in enumerate(image_list):
                if not _should_extract_image(img, xreflist, config, doc):
                    continue

                # Criar pasta apenas quando for salvar a primeira imagem
                if not folder_created:
                    output_path.mkdir(parents=True, exist_ok=True)
                    folder_created = True
                    stats["output_path"] = str(output_path)
                    print(f"✓ Pasta criada: {output_path}")

                context = ImageSaveContext(
                    img=img, doc=doc, output_path=output_path,
                    page_num=page_num, img_index=img_index, xreflist=xreflist
                )
                stats["extracted"] += _extract_and_save_image(context)

        doc.close()
        
        # Se nenhuma imagem foi extraída, informar e não criar pasta
        if stats["extracted"] == 0:
            print(f"\n⚠ Nenhuma imagem foi extraída do PDF.")
            print(f"Motivos possíveis:")
            print(f"  • PDF não contém imagens")
            print(f"  • Todas as imagens foram filtradas pelos critérios:")
            print(f"    - dimlimit={config.dimlimit} (dimensão mínima)")
            print(f"    - abssize={config.abssize} (tamanho mínimo em bytes)")
            print(f"    - relsize={config.relsize} (densidade mínima)")
            print(f"  • Pasta não foi criada pois não há imagens para salvar")
        
        return stats

    except FileNotFoundError as e:
        print(f"Erro: Arquivo PDF não encontrado: {e}")
        raise
    except OSError as e:
        print(f"Erro ao acessar arquivo: {e}")
        raise


def _extract_and_save_image(context: ImageSaveContext) -> int:
    """Extrai e salva uma imagem, retornando 1 se bem-sucedido, 0 caso contrário."""
    image = recoverpix(context.doc, context.img)
    xref = context.img[0]
    width = context.img[2]
    height = context.img[3]
    imgdata = image["image"]

    # Salvar imagem
    image_page = f"page_{context.page_num + 1}_img_{context.img_index + 1}.{image['ext']}"
    imgfile = context.output_path / image_page

    with open(imgfile, "wb") as fout:
        fout.write(imgdata)

    context.xreflist.append(xref)
    print(f"  ✓ {imgfile.name} ({width}x{height}px, {len(imgdata)/1024:.1f}KB)")

    return True
