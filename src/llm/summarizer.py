"""
src/llm/summarizer.py

Este módulo fornece a classe `Summarizer`, que encapsula o carregamento do modelo
e tokenizer, e oferece métodos para:

- Verificar a quantidade de tokens de um texto (`check_token_length`).
- Dividir textos grandes em chunks (`chunk_text`).
- Gerar resumos de textos, lidando automaticamente com textos que excedem
  o limite de tokens do modelo (`summarize_text`).

"""

import math
from typing import List
from .model_loader import model_loader

MODEL_MAX_LENGTH = 32768

class Summarizer:
    """
    Componente de modelo (LLM) que encapsula carregamento do modelo/tokenizer
    e oferece métodos para resumir textos. Projetado para ser instanciado e
    usado pelo Controller no padrão MVC.
    """

    def __init__(self, model=None, tokenizer=None):

        if model is None or tokenizer is None:
            model, tokenizer = model_loader()
        self.model = model
        self.tokenizer = tokenizer


    def check_token_length(self, text: str, max_length: int):
        """
        Checa o tamanho da entrada de texto e verifica a compatibilidade do modelo
        Docstring for check_token_length

        :param self: Description
        :param text: Description
        :type text: str
        :param max_length: Description
        :type max_length: int
        """
        tokens = self.tokenizer.encode(text, add_special_tokens=False)
        num_tokens = len(tokens)
        exceeds = num_tokens > max_length
        overflow = num_tokens - max_length if exceeds else 0

        return {
            'num_tokens': num_tokens,
            'exceeds_limit': exceeds,
            'max_length': max_length,
            'overflow_tokens': overflow
        }

    def chunk_text(self, text: str, max_chunk_tokens: int) -> List[str]:
        """Divide o texto em chunks com base no número máximo de tokens por chunk."""
        tokens = self.tokenizer.encode(text, add_special_tokens=False)
        chunks = []
        max_tokens = int(math.ceil(len(tokens)/max_chunk_tokens))
        # Iterar pelos tokens em passos de tamanho max_chunk_tokens
        for i in range(0, len(tokens), max_tokens):
            chunk_tokens = tokens[i:i + max_tokens]
            chunk_text = self.tokenizer.decode(chunk_tokens, skip_special_tokens=True)
            chunks.append(chunk_text)

        print(f"Texto dividido em {len(chunks)} chunks.")
        return chunks

    def _generate_summary_from_prompt(self, prompt: str, max_output_tokens: int) -> str:
        """Gera resumo a partir de um prompt (reutilizável para small/large text).

        Encapsula a lógica de tokenização, geração e decodificação.
        Reduz duplicação de código e variáveis locais.
        """
        input_ids = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        output = self.model.generate(
            **input_ids,
            max_new_tokens=max_output_tokens,
            do_sample=True,
            temperature=0.3,
            top_k=40,
            top_p=0.9,
            repetition_penalty=1.1,
            pad_token_id=self.tokenizer.eos_token_id
        )

        decoded = self.tokenizer.decode(output[0], skip_special_tokens=True)
        summary = decoded.split("assistant\n")[-1].strip()

        return summary

    def _summarize_small_text(self, full_prompt: str, max_output_tokens: int) -> str:
        """Gera resumo quando o texto cabe na janela de contexto.

        Recebe o full_prompt e produz o resumo final.
        """
        print("\nGerando resumo final (contexto cabe no prompt)...")
        return self._generate_summary_from_prompt(full_prompt, max_output_tokens)

    def _summarize_chunks(self, chunks: List[str], max_output_tokens: int) -> List[str]:
        """Resume cada chunk individualmente.

        Encapsula a lógica de iteração e geração de resumos de chunks.
        Reduz variáveis locais na função pai (_summarize_large_text).
        """
        chunk_summaries = []

        for idx, chunk in enumerate(chunks, 1):
            print(f"\n📦 Resumindo chunk {idx}/{len(chunks)}...")

            messages = [
                {"role": "system", "content": "Você resume textos em português de forma clara."},
                {"role": "user", "content": f"Resuma o seguinte trecho:\n\n{chunk}"}
            ]

            prompt = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )

            summary = self._generate_summary_from_prompt(prompt, max_output_tokens)
            chunk_summaries.append(summary)

        return chunk_summaries

    def _consolidate_summaries(self, summaries: List[str], max_output_tokens: int) -> str:
        """Consolida múltiplos resumos em um único resumo final.

        Encapsula a lógica de consolidação de resumos de chunks.
        Reduz variáveis locais na função pai (_summarize_large_text).
        """
        print("\n🔗 Consolidando chunks...")

        combined = "\n\n".join(summaries)

        messages = [
            {"role": "system",
            "content": "Você consolida múltiplos resumos em apenas um, de forma coerente."},
            {"role": "user",
            "content": f"Consolide estes resumos:\n\n{combined}"}
        ]

        prompt = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        return self._generate_summary_from_prompt(prompt, max_output_tokens)

    def _summarize_large_text(self, text: str, max_output_tokens: int = 512) -> str:
        """Processa textos maiores que a janela de contexto usando chunking.

        Divide o texto em chunks, resume cada um e, se necessário,
        consolida os resumos em um resumo final.
        """
        print("\n  Texto muito grande, aplicando chunking")

        chunks = self.chunk_text(text)
        chunk_summaries = self._summarize_chunks(chunks, max_output_tokens)
        final_summary = ''
        if len(chunk_summaries) > 1:
            final_summary = self._consolidate_summaries(chunk_summaries, max_output_tokens)
        else:
            final_summary = chunk_summaries[0]
        return final_summary

    def summarize_text(self, text: str, max_output_tokens: int) -> str:
        """Faz o resumo do texto com uso do modelo Qwen-3B"""

        # Preparar mensagens/prompt
        messages = [
            {"role": "system",
             "content": "Você é um assistente que resume textos de forma clara e objetiva."},
            {"role": "user", "content": f"Resuma o seguinte texto:\n\n{text}"}
        ]

        full_prompt = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        # Verificar se cabe no contexto
        token_info = self.check_token_length(full_prompt,
                                            MODEL_MAX_LENGTH)

        print("\n--- VERIFICAÇÃO DE TOKEN ---")
        print(f"Tokens totais: {token_info['num_tokens']}")
        print(f"Limite: {token_info['max_length']}")
        print(f"Excede? {token_info['exceeds_limit']}")

        if token_info['exceeds_limit']:
            # Texto grande -> usar pipeline de chunking
            summary = self._summarize_large_text(text, max_output_tokens=max_output_tokens)
        else:
            # Texto cabe no contexto -> gerar diretamente
            summary = self._summarize_small_text(full_prompt, max_output_tokens)
        return summary
