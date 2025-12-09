import pymupdf4llm
import pymupdf # PyMuPDF is imported as fitz

def extract_and_print_headers(pdf_path):
    # Open the PDF document
    doc = pymupdf.open(pdf_path)

    # Convert the document to Markdown. 
    # By default, this will automatically identify headers based on font sizes.
    markdown_text = pymupdf4llm.to_markdown(doc)
    print(markdown_text)
    doc.close()

    # Split the markdown text into lines and filter for headers (lines starting with '#')
    headers = []
    for line in markdown_text.splitlines():
        if line.strip().startswith('#'):
            headers.append(line.strip())

    if headers:
        levels = []
        for header in headers:
            # The number of '#' indicates the header level
            level = header.count('#')
            levels.append((level, header))
            print(levels)
            # text = header.lstrip('#').strip()
            # print(f"{level}: {text}")
        
        #Verificar se a titulo
        has_title = False
        index = {}
        for level in levels:
            if level[0] == 1 and not has_title:
                has_title = True
            index[level[0]] = index.get(level[0], 0) + 1
        
        
        for level in levels:
            print(f"{level[0]}:{index.get(level[0])}")
            if level[0] == 1 and has_title:
                print(f"Title: {level[1].lstrip('#').strip("* ")}")
            else:
                print(f"Header Level {level[0]}: {level[1].lstrip('#').strip("*.0123456789 ")}")
        print("------------------------------------------")
    else:
        print(f"No headers identified in {pdf_path}.")

# Example usage:
# Make sure you have a PDF file named 'input.pdf' in the same directory


extract_and_print_headers("C:/Users/jc130/OneDrive/Área de Trabalho/Desafio_Python/public/arquivo_pdf/4-Vetebrados.pdf")