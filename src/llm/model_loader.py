"""
src/llm/model_loader.py

Este módulo fornece a função `model_loader`, que realiza o carregamento
do modelo de linguagem e seu tokenizer de forma automática, configurando
os parâmetros adequados para uso em GPU/CPU conforme disponível
"""

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

MODEL_NAME = "Qwen/Qwen2.5-3B"

def model_loader():
    """
    Docstring for model_loader
    """
    print(" Carregando modelo uma única vez...")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model =AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        dtype=torch.float16,
        device_map="auto"
    )

    print(" Modelo carregado e pronto para uso!")
    return model, tokenizer
