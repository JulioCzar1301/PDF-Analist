"""
src/pdf/headers.py

Este módulo fornece utilitários para extrair cabeçalhos (headings) de um
documento PDF e gerar uma versão enumerada e normalizada em texto, útil para
criar sumários ou índices. A extração usa `pymupdf` para abrir o PDF e
`pymupdf4llm.to_markdown` para converter o conteúdo em markdown bruto, a partir
do qual os cabeçalhos são identificados e numerados.
"""

import pymupdf4llm
import pymupdf


def clean_header_text(header):
    """Remove caracteres especiais e números do texto do cabeçalho."""
    return header.lstrip('#').strip(' *.0123456789 ').strip()


def normalize_header_levels(headers_with_levels, offset):
    """Normaliza os níveis dos cabeçalhos aplicando um offset."""
    normalized = []
    for level, header in headers_with_levels:
        new_level = max(level - offset, 1)
        normalized.append((new_level, header))
    return normalized


def calculate_numbering(counters, level, title_exists=False, min_level=1):
    """Calcula a numeração hierárquica para um cabeçalho."""
    if title_exists:
        if level == min_level + 1:
            return f"{counters[2]}"
        if level == min_level + 2:
            return f"{counters[2]}.{counters[3]}"
        parts = [str(counters[i]) for i in range(1, level + 1)]
    else:
        if level == 1:
            return f"{counters[1]}"
        if level == 2:
            return f"{counters[1]}.{counters[2]}"
        if level == 3:
            return f"{counters[1]}.{counters[2]}.{counters[3]}"
        parts = [str(counters[i]) for i in range(1, level + 1)]
    return ".".join(parts)


def update_counters(counters, level, previous_level):
    """Atualiza os contadores hierárquicos baseados no nível atual."""
    if level == previous_level:
        counters[level] += 1
    elif level > previous_level:
        counters[level] = 1
    else:
        counters[level] += 1

    # Zera contadores de níveis inferiores
    for x in range(level + 1, 7):
        counters[x] = 0

    return counters


def process_title_detection(levels):
    """Detecta e processa título se existir um único cabeçalho do nível mínimo."""
    min_level = min(level for level, _ in levels)
    headers_min_level = [h for level, h in levels if level == min_level]

    title = None
    if len(headers_min_level) == 1:
        title_text = clean_header_text(headers_min_level[0])
        title = f"Title: {title_text}"
        # Remove o título da lista de níveis
        levels = [(lvl, h) for (lvl, h) in levels if h != headers_min_level[0]]

    return levels, title, min_level


def process_header_levels(levels, has_title, min_level):
    """Processa todos os cabeçalhos e gera a saída formatada."""
    output = []
    counters = {i: 0 for i in range(1, 7)}
    previous_level = min_level

    for current_level, header in levels:
        # Limita o nível ao máximo permitido
        current_level = min(current_level, previous_level + 1)

        # Limpa o texto
        text = clean_header_text(header)

        # Atualiza contadores
        counters = update_counters(counters, current_level, previous_level)

        # Calcula numeração
        num = calculate_numbering(counters, current_level, has_title, min_level)
        output.append(f"{num}. {text}")

        previous_level = current_level

    return output


def extract_headers(pdf_path):
    """Extrai e normaliza cabeçalhos de um PDF.

    Abre o PDF em `pdf_path`, converte seu conteúdo para markdown bruto e
    identifica linhas que representam cabeçalhos (linhas que começam com
    '#'). Em seguida normaliza os níveis de cabeçalho (garantindo que o
    primeiro nível encontrado passe a ser nível 1), detecta um possível
    título e gera numeração hierárquica coerente para os headings.

    Parâmetros
    -----------
    pdf_path : str | Path
        Caminho para o arquivo PDF a ser processado.

    Retorna
    -------
    str
        Uma string contendo os cabeçalhos numerados, separados por quebras de
        linha. Se nenhum cabeçalho for encontrado, retorna mensagem indicando
        que não foram identificados cabeçalhos válidos.
    """
    # Extração inicial do markdown
    doc = pymupdf.open(pdf_path)
    markdown_text = pymupdf4llm.to_markdown(doc)

    # Identifica cabeçalhos brutos
    headers = [
        line.strip()
        for line in markdown_text.splitlines()
        if line.strip().startswith('#')
    ]

    if not headers:
        return "No valid headers identified."

    # Processa níveis iniciais
    levels = [(header.count('#'), header) for header in headers]
    first_level = levels[0][0]
    offset = first_level - 1

    # Normaliza níveis
    levels = normalize_header_levels(levels, offset)

    # Detecta título
    levels, title, min_level = process_title_detection(levels)

    # Processa cabeçalhos
    output = []
    if title:
        output.append("\n" + title)

    has_title = bool(title)
    formatted_headers = process_header_levels(levels, has_title, min_level)
    output.extend(formatted_headers)

    return "\n".join(output)
