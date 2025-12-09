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

import pymupdf as fitz
import os


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
        pix0 = fitz.Pixmap(doc.extract_image(xref)["image"])
        if pix0.alpha:  # remove canal alpha se já existir
            pix0 = fitz.Pixmap(pix0, 0)
        mask = fitz.Pixmap(doc.extract_image(smask)["image"])

        try:
            pix = fitz.Pixmap(pix0, mask)
        except:  # fallback para imagem original se houver problema
            pix = fitz.Pixmap(doc.extract_image(xref)["image"])

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
        pix = fitz.Pixmap(doc, xref)
        pix = fitz.Pixmap(fitz.csRGB, pix)
        return {
            "ext": "png",
            "colorspace": 3,
            "image": pix.tobytes("png"),
        }
    
    # Caso padrão: extração direta
    return doc.extract_image(xref)


def extract_images_from_pdf(
    pdf_path: Union[str, Path],
    output_dir: Union[str, Path],
    dimlimit: int = 0,
    relsize: float = 0.0,
    abssize: int = 0,
) -> Dict[str, Union[int, str]]:
    """
    Extrai imagens de um arquivo PDF com filtros opcionais.
    
    Parâmetros:
    -----------
    pdf_path : str
        Caminho do arquivo PDF
    output_dir : str
        Diretório de saída
    dimlimit : int
        Dimensão mínima (largura ou altura). Ex: 100 = ignora imagens < 100px
    relsize : float
        Tamanho relativo mínimo. Ex: 0.05 = ignora se < 5% do tamanho teórico
    abssize : int
        Tamanho absoluto mínimo em bytes. Ex: 2048 = ignora se < 2KB
    """
    try:
        # Nome do arquivo PDF (ex: 'artigo')
        pdf_filename: str = Path(pdf_path).stem  # sem extensão

        # Criar pasta de saída
        output_path: Path = Path(output_dir) / pdf_filename
        output_path.mkdir(parents=True, exist_ok=True)

        # Abrir PDF
        doc = fitz.open(str(pdf_path))
        
        # Lista para evitar duplicatas (mesma imagem em várias páginas)
        xreflist: list[int] = []
        total_images: int = 0
        extracted_images: int = 0
        
        # Iterar por cada página
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Obter lista de imagens da página (com informações completas)
            image_list = page.get_images(full=True)
            total_images += len(image_list)
            
            print(f"Página {page_num + 1}: {len(image_list)} imagem(ns) encontrada(s)")
            
            for img_index, img in enumerate(image_list):
                xref: int = img[0]
                
                # Verificar se já extraímos esta imagem
                if xref in xreflist:
                    print(f"  → Imagem {xref} já extraída (duplicata)")
                    continue
                
                # Obter dimensões
                width: int = img[2]
                height: int = img[3]
                
                # Filtro: dimensão mínima
                if min(width, height) <= dimlimit:
                    print(f"  → Imagem {xref} muito pequena ({width}x{height})")
                    continue
                
                # Recuperar imagem (com tratamento de casos especiais)
                image = recoverpix(doc, img)
                n: int = image["colorspace"]
                imgdata: bytes = image["image"]
                
                # Filtro: tamanho absoluto mínimo
                if len(imgdata) <= abssize:
                    print(f"  → Imagem {xref} arquivo muito pequeno ({len(imgdata)} bytes)")
                    continue
                
                # Filtro: tamanho relativo (densidade)
                if width * height * n > 0:  # evitar divisão por zero
                    if len(imgdata) / (width * height * n) <= relsize:
                        print(f"  → Imagem {xref} densidade muito baixa")
                        continue
                
                # Salvar imagem
                imgfile: Path = output_path / f"page_{page_num + 1}_img_{img_index + 1}_xref_{xref}.{image['ext']}"
                
                with open(imgfile, "wb") as fout:
                    fout.write(imgdata)
                
                xreflist.append(xref)
                extracted_images += 1
                
                print(f"  ✓ {imgfile.name} ({width}x{height}px, {len(imgdata)/1024:.1f}KB)")
        
        doc.close()
        
        # Resumo
        print(f"\n{'='*60}")
        print(f"PDF: {pdf_filename}")
        print(f"Total de imagens no documento: {total_images}")
        print(f"Imagens únicas encontradas: {len(set(xreflist))}")
        print(f"Imagens extraídas: {extracted_images}")
        print(f"Pasta de saída: {output_path}")
        print(f"{'='*60}")
        
        return {
            "total": total_images,
            "extracted": extracted_images,
            "output_path": str(output_path),
        }
        
    except Exception as e:
        print(f"Erro ao extrair imagens: {e}")
        raise
