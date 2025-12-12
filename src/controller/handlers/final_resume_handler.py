"""
src/controller/handlers/final_resume_handler.py

Handler para geração do relatório final completo em Markdown.
"""

import os
from typing import Any
from textwrap import dedent
from .base_handler import BaseHandler
from .resume_handler import ResumeHandler


class FinalResumeHandler(BaseHandler):
    """
    Handler responsável por gerar o relatório final completo.

    Funcionalidades:
    - Agrega todas as informações do PDF
    - Gera resumo com LLM
    - Cria documento Markdown estruturado
    - Salva arquivo no mesmo diretório do PDF
    """

    def handle_final_resume(self, model: Any, llm_model: Any, tokenizer: Any) -> None:
        """
        Gera relatório final em Markdown com todas as informações.

        O relatório inclui:
        - Informações gerais (páginas, palavras, tamanho)
        - Top 10 palavras mais frequentes
        - Estrutura do documento
        - Resumo gerado por LLM

        Args:
            model: Modelo PDFModel com os dados do documento.
            llm_model: Modelo LLM pré-carregado (ou None).
            tokenizer: Tokenizer pré-carregado (ou None).
        """
        self.logger.info("Gerando relatório final completo")

        try:
            # Obter informações gerais
            self.logger.debug("Coletando informações gerais do PDF")
            info_pdf = model.get_summary()

            # Gerar resumo com LLM
            self.logger.debug("Gerando resumo com LLM")
            resume_handler = ResumeHandler(self.view, self.logger)
            resume = resume_handler.handle_resume(model, llm_model, tokenizer)

            if not resume:
                self.logger.warning("Resumo vazio, continuando com informações básicas")
                resume = "Não foi possível gerar resumo."

            # Montar documento Markdown
            markdown_content = self._build_markdown(info_pdf, resume)

            # Salvar arquivo
            output_file = self._save_file(model.pdf_path, markdown_content)

            self.logger.info(f"Relatório final salvo com sucesso: {output_file}")
            self.view.render_success(f"Relatório final salvo em: {output_file}")

        except Exception as e:
            self.logger.exception(f"Erro ao gerar relatório final: {e}")
            self.view.render_error(f"Erro ao gerar relatório final: {e}")


    def _build_markdown(self, info_pdf: dict, resume: str) -> str:
        """
        Constrói o conteúdo Markdown do relatório.

        Args:
            info_pdf: Dicionário com informações do PDF.
            resume: Resumo gerado pelo LLM.

        Returns:
            str: Conteúdo completo do relatório em Markdown.
        """
        content = dedent(f"""\
        ## INFORMAÇÕES GERAIS DO PDF
        - **Arquivo**: {info_pdf["file"]}
        - **Páginas**: {info_pdf["page_count"]}
        - **Palavras**: {info_pdf["word_count"]}
        - **Tamanho em Bytes**: {info_pdf["byte_size"]}
        - **Tamanho do vocabulário**: {info_pdf["vocabulary"]}

        ### PALAVRAS MAIS FREQUENTES:
        """)

        # Adicionar palavras frequentes
        for palavra, frequencia in info_pdf["word_freq"]:
            content += f"- {palavra}: {frequencia}\n"

        # Adicionar estrutura
        content += dedent(f"""\
        ### ESTRUTURA DO TEXTO
        {info_pdf["headers"].strip()}
        """)

        # Adicionar resumo
        content += dedent(f"""\
        ### RESUMO
        {resume.strip()}
        """)

        return content


    def _save_file(self, pdf_path: str, content: str) -> str:
        """
        Salva o conteúdo em arquivo Markdown.

        O arquivo é salvo no mesmo diretório do PDF original,
        com o nome: <nome_original>_resumo_final.md

        Args:
            pdf_path: Caminho do arquivo PDF original.
            content: Conteúdo a ser salvo.

        Returns:
            str: Caminho completo do arquivo salvo.
        """
        # Extrair nome base sem extensão
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]

        # Construir caminho de saída
        output_dir = os.path.dirname(pdf_path) or "."
        output_file = os.path.join(output_dir, f"{base_name}_resumo_final.md")

        self.logger.debug(f"Salvando relatório em: {output_file}")

        # Salvar arquivo
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)

        return output_file