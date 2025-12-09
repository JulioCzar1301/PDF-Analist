# summarizer.py
import math
from llm.model_loader import model_loader

model, tokenizer = model_loader()


# -------- FUNÇÕES AUXILIARES -------- #

def check_token_length(text: str, max_length: int = MAX_CONTEXT_LENGTH):
    tokens = tokenizer.encode(text, add_special_tokens=False)
    num_tokens = len(tokens)
    exceeds = num_tokens > max_length
    overflow = num_tokens - max_length if exceeds else 0

    return {
        'num_tokens': num_tokens,
        'exceeds_limit': exceeds,
        'max_length': max_length,
        'overflow_tokens': overflow
    }


def chunk_text(text: str, max_chunk_tokens: int = 28000):
    tokens = tokenizer.encode(text, add_special_tokens=False)
    chunks = []
    max_chunks = int(len(tokens)/math.ceil((len(tokens)/max_chunk_tokens)))
    print("O que deveria ser o tamanho dos chunks: ", max_chunks)
    for i in range(0, len(tokens), max_chunks):
        chunk_tokens = tokens[i:i + max_chunk_tokens]
        chunk_text = tokenizer.decode(chunk_tokens, skip_special_tokens=True)
        chunks.append(chunk_text)

    print(f"Texto dividido em {len(chunks)} chunks.")
    return chunks


# -------- FUNÇÃO PRINCIPAL DE RESUMO -------- #

def summarize_text(text: str, max_output_tokens: int = 512) -> str:

    messages = [
        {"role": "system", "content": "Você é um assistente que resume textos de forma clara e objetiva em português."},
        {"role": "user", "content": f"Resuma o seguinte texto:\n\n{text}"}
    ]

    full_prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    # Verificar se cabe no contexto
    token_info = check_token_length(full_prompt)

    print("\n--- VERIFICAÇÃO DE TOKEN ---")
    print(f"Tokens totais: {token_info['num_tokens']}")
    print(f"Limite: {token_info['max_length']}")
    print(f"Excede? {token_info['exceeds_limit']}")

    # ============================================================
    # CASO EXCEDA A JANELA DE CONTEXTO → USAR CHUNKING
    # ============================================================

    if token_info['exceeds_limit']:
        print("\n⚠️  Texto muito grande, aplicando chunking...")

        chunks = chunk_text(text)

        chunk_summaries = []

        # ----- Resumir cada chunk -----
        for idx, chunk in enumerate(chunks, 1):
            print(f"\n📦 Resumindo chunk {idx}/{len(chunks)}...")

            chunk_messages = [
                {"role": "system", "content": "Você resume textos em português de forma clara."},
                {"role": "user", "content": f"Resuma o seguinte trecho:\n\n{chunk}"}
            ]

            chunk_prompt = tokenizer.apply_chat_template(
                chunk_messages,
                tokenize=False,
                add_generation_prompt=True
            )

            input_ids = tokenizer(chunk_prompt, return_tensors="pt").to(model.device)

            output = model.generate(
                **input_ids,
                max_new_tokens=max_output_tokens,
                do_sample=True,
                temperature=0.3,
                top_k=40,
                top_p=0.9,
                repetition_penalty=1.1,
                pad_token_id=tokenizer.eos_token_id
            )

            text_out = tokenizer.decode(output[0], skip_special_tokens=True)
            summary = text_out.split("assistant\n\n")[-1].strip()
            chunk_summaries.append(summary)

        # ----- Consolidar os resumos dos chunks -----

        if len(chunk_summaries) > 1:
            print("\n🔗 Consolidando chunks...")

            combined_chunks = "\n\n".join(chunk_summaries)

            final_messages = [
                {"role": "system", "content": "Você consolida múltiplos resumos em apenas um, de forma coerente."},
                {"role": "user", "content": f"Consolide estes resumos:\n\n{combined_chunks}"}
            ]

            final_prompt = tokenizer.apply_chat_template(
                final_messages,
                tokenize=False,
                add_generation_prompt=True
            )

            input_ids = tokenizer(final_prompt, return_tensors="pt").to(model.device)

            output = model.generate(
                **input_ids,
                max_new_tokens=max_output_tokens,
                do_sample=True,
                temperature=0.3,
                top_k=40,
                top_p=0.9,
                repetition_penalty=1.1,
                pad_token_id=tokenizer.eos_token_id
            )

            consolidated = tokenizer.decode(output[0], skip_special_tokens=True)
            final_summary = consolidated.split("assistant\n\n")[-1].strip()

            return final_summary

        else:
            return chunk_summaries[0]

    # ============================================================
    # SE CABE NO CONTEXTO → RESUMO DIRETO
    # ============================================================

    input_ids = tokenizer(full_prompt, return_tensors="pt").to(model.device)

    print("\nGerando resumo final...")

    output = model.generate(
        **input_ids,
        max_new_tokens=max_output_tokens,
        do_sample=True,
        temperature=0.3,
        top_k=40,
        top_p=0.9,
        repetition_penalty=1.1,
        pad_token_id=tokenizer.eos_token_id
    )

    final = tokenizer.decode(output[0], skip_special_tokens=True)
    final_summary = final.split("assistant\n")[-1].strip()

    return final_summary
