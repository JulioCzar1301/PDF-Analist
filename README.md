# PDF Analyzer

Sistema de análise e extração de informações de arquivos PDF com suporte a extração de imagens e geração de resumos usando LLM local.

## 📋 Requisitos

- Python 3.9+
- pip (gerenciador de pacotes Python)
- Mínimo 16GB de RAM (recomendado para o modelo LLM)

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd <nome-do-diretorio>
```

### 2. Crie um ambiente virtual

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

## 🚀 Como rodar o projeto

### Execução básica

```bash
python main.py <caminho_do_pdf> [opções]
```

### Aviso (download do modelo)

O sistema fará download automático do modelo Qwen 3B, quando for solicitado o resumo ou o relatorio final (~6GB):

```bash
python main.py documento.pdf -info
```

**Aguarde o download ser concluído.** Após a primeira execução, o modelo ficará em cache local.

### Fluxo completo recomendado

Para análise completa do PDF em um único comando:

```bash
python main.py documento.pdf -final_resume
```

Isso irá:
1. Analisar o PDF (páginas, palavras, vocabulário)
2. Calcular palavras mais frequentes
3. Extrair a estrutura do documento
4. Gerar resumo com LLM
5. Salvar relatório completo em Markdown

## ✨ Funcionalidades implementadas

### 📄 Funcionalidades obrigatórias

#### 1. Análise do PDF
✅ **Extração e exibição de informações** (sem uso de IA):
- Número total de páginas
- Número total de palavras
- Tamanho do arquivo em bytes
- Top 10 palavras mais comuns (excluindo stopwords)
- Tamanho do vocabulário (palavras distintas após limpeza)

**Comandos:**
```bash
python main.py documento.pdf -page_count        # Número de páginas
python main.py documento.pdf -words_count       # Total de palavras
python main.py documento.pdf -best_words        # Top 10 palavras
python main.py documento.pdf -vocabulary_size   # Tamanho do vocabulário
python main.py documento.pdf -info              # Todas as informações acima
```

#### 2. Extração de Imagens
✅ **Identificação e extração de imagens**:
- Salva em diretório `extracted_images/<nome-pdf>/`
- Nomes únicos para cada imagem
- Filtros configuráveis (dimensão mínima, tamanho do arquivo)
- Suporte a diretório customizado

**Comando:**
```bash
python main.py documento.pdf -extract_images
```

**Com configurações personalizadas:**
```bash
python main.py documento.pdf -extract_images \
    --output_dir ./minhas_imagens \
    --dimlimit 100 \
    --abssize 2048
```

#### 3. Geração de Resumo com LLM Local
✅ **Modelo Qwen 3B executado localmente**:
- Carregamento automático do modelo da Hugging Face
- Geração de resumo textual do conteúdo
- Exibição no terminal
- Salvamento opcional em arquivo Markdown

**Comando:**
```bash
python main.py documento.pdf -resume
```

### 🌟 Funcionalidades opcionais implementadas

✅ **Detecção de estrutura do documento**
- Identificação automática de títulos e seções
- Hierarquia de cabeçalhos
- Extração de estrutura organizacional

```bash
python main.py documento.pdf -text_structure
```

✅ **Suporte a PDFs grandes**
- Arquitetura Map-Reduce para textos que excedem limite de tokens
- Chunking inteligente (28.000 tokens por chunk)
- Consolidação automática de resumos parciais
- Tratamento de exceções robusto

✅ **Limpeza e normalização avançada**
- Remoção de caracteres especiais
- Normalização de espaços e quebras de linha
- Tratamento de encoding
- Remoção de stopwords do português brasileiro

✅ **Sistema de logs completo**
- Logs salvos em arquivo (`./logs/app.log`)
- Rastreamento de operações
- Informações de debug sobre tokenização e chunking

✅ **Relatório unificado em Markdown**
- Comando `-final_resume` gera documento completo
- Inclui todas as análises em um único arquivo
- Formato profissional e organizado

```bash
python main.py documento.pdf -final_resume
```

✅ **Organização modular do código**
- Estrutura MVC clara
- Separação por responsabilidades
- Pacotes bem definidos (cli, controller, llm, pdf, utils)

✅ **Tipagem com typing**
- Type hints em todas as funções
- Melhor documentação e IDE support
- Código mais robusto e manutenível

## 🎯 O que deve ser avaliado

### 1. Qualidade do código
- **Arquitetura MVC**: Separação clara entre CLI, Controller e Model (LLM)
- **Modularização**: Pacotes organizados por responsabilidade (cli, controller, llm, pdf, utils)
- **Tipagem forte**: Type hints em todas as funções usando `typing`
- **Documentação**: Docstrings detalhadas em todos os módulos e funções
- **Boas práticas**: Código limpo, nomes descritivos, funções com responsabilidade única

### 2. Domínio de Python
- **Orientação a objetos**: Classes bem estruturadas (`Summarizer`, `Controller`)
- **List comprehensions**: Uso eficiente de estruturas pythônicas
- **Context managers**: Gerenciamento adequado de recursos
- **Bibliotecas padrão**: Uso eficiente de `argparse`, `pathlib`, `logging`, `typing`
- **Tratamento de erros**: Try-except estratégicos para robustez

### 3. Integração com LLM
- **Modelo local**: Qwen 3B rodando sem dependências externas/APIs
- **Carregamento eficiente**: Cache do modelo após primeira execução
- **Parâmetros otimizados**: Temperature, top_k, top_p ajustados para resumos consistentes
- **Gestão de memória**: Uso eficiente de GPU/CPU
- **Prompts estruturados**: Chat templates para melhor controle

### 4. Estrutura do projeto
- **Hierarquia clara**: Separação lógica em pacotes
- **Configurações centralizadas**: Parâmetros de imagem, stopwords organizadas
- **Reutilização**: Funções utilitárias para operações comuns
- **Escalabilidade**: Fácil adicionar novas funcionalidades

### 5. Fidelidade ao escopo
- ✅ **Todas as funcionalidades obrigatórias implementadas**
- ✅ **Análise sem IA**: Contagem e frequência com bibliotecas Python puras
- ✅ **Extração de imagens**: Com nomes únicos e diretório configurável
- ✅ **LLM local**: Qwen 3B da Hugging Face, sem APIs externas
- ✅ **Saída padrão**: Todas as informações exibidas no terminal

### 6. Funcionalidades extras (diferenciais)

**🏆 Implementações que agregam valor:**

1. **Arquitetura Map-Reduce completa**
   - Processamento distribuído de documentos grandes
   - Chunking inteligente baseado em tokens
   - Consolidação hierárquica de resumos

2. **Sistema de logs profissional**
   - Arquivo de log estruturado
   - Rastreamento completo de operações
   - Útil para debug e auditoria

3. **Detecção de estrutura avançada**
   - Identificação automática de hierarquia
   - Extração de títulos e seções
   - Organização lógica do documento

4. **Relatório Markdown completo**
   - Documento único com todas as análises
   - Formato profissional e exportável
   - Fácil compartilhamento

5. **Normalização robusta de texto**
   - Limpeza avançada de caracteres
   - Tratamento de encoding
   - Remoção inteligente de stopwords

6. **Configurabilidade total**
   - Filtros de imagem ajustáveis
   - Diretórios personalizáveis
   - Parâmetros flexíveis via CLI

**Por que avaliar esses diferenciais:**
- Demonstram compreensão profunda de processamento de texto
- Mostram capacidade de resolver problemas complexos (textos grandes)
- Evidenciam preocupação com usabilidade e manutenibilidade
- Aplicam conceitos avançados (Map-Reduce, gestão de contexto de LLMs)
- Tornam o sistema robusto e pronto para produção

## 💻 Uso

### Sintaxe básica

```bash
python main.py <caminho_do_pdf> [opções]
```

### Opções disponíveis

| Opção | Descrição |
|-------|-----------|
| `-info` | Exibe informações gerais do PDF |
| `-page_count` | Mostra o número de páginas |
| `-words_count` | Contagem total de palavras |
| `-best_words` | Lista as palavras mais frequentes |
| `-vocabulary_size` | Tamanho do vocabulário único |
| `-text_structure` | Estrutura e hierarquia do texto |
| `-resume` | Gera resumo do conteúdo |
| `-extract_images` | Extrai imagens do PDF |
| `-final_resume` | Gera relatório completo com todas as informações |

### Opções de extração de imagens

| Parâmetro | Descrição | Padrão |
|-----------|-----------|--------|
| `--output_dir` | Diretório de saída para imagens | `./extracted_images` |
| `--dimlimit` | Dimensão mínima (largura/altura) em pixels | `50` |
| `--abssize` | Tamanho mínimo do arquivo em bytes | `1024` |

## 📖 Exemplos de uso

### Análise completa

```bash
python main.py documento.pdf -final_resume
```

### Informações básicas

```bash
python main.py documento.pdf -info
```

### Extrair apenas imagens

```bash
python main.py documento.pdf -extract_images --output_dir ./minhas_imagens
```

### Extrair imagens com filtros personalizados

```bash
python main.py documento.pdf -extract_images --dimlimit 100 --abssize 2048
```

### Múltiplas análises

```bash
python main.py documento.pdf -page_count -words_count -best_words
```

### Análise estrutural e resumo

```bash
python main.py documento.pdf -text_structure -resume
```

## 📊 Logs

O sistema gera logs automáticos durante a execução:

- **Local**: Os logs são salvos no diretório `./logs/`
- **Arquivo**: `app.log` (criado automaticamente)
- **Conteúdo**: Informações sobre:
  - Verificação de tokens
  - Processo de chunking de texto
  - Geração de resumos
  - Consolidação de chunks
  - Erros e avisos

### Exemplo de saída de log

```
--- VERIFICAÇÃO DE TOKEN ---
Tokens totais: 45230
Limite: 32768
Excede? True

  Texto muito grande, aplicando chunking
Texto dividido em 2 chunks.

📦 Resumindo chunk 1/2...
📦 Resumindo chunk 2/2...

🔗 Consolidando chunks...
```

## 📁 Estrutura do projeto

```
.
├── main.py                      # Ponto de entrada da aplicação
├── requirements.txt             # Dependências do projeto
├── src/
│   ├── cli/
│   │   ├── __init__.py         # Inicialização do pacote CLI
│   │   ├── arguments.py        # Parser de argumentos da linha de comando
│   │   └── views.py            # Formatação e exibição de resultados
│   │
│   ├── controller/
│   │   ├── __init__.py         # Inicialização do pacote Controller
│   │   ├── controller.py       # Orquestração da lógica de negócio (MVC)
│   │   └── handlers/
│   │       ├── __init__.py                    # Exportação de todos os handlers
│   │       ├── base_handler.py                # Classe base (~20 linhas)
│   │       ├── info_handler.py                # Informações gerais (~40 linhas)
│   │       ├── text_analysis_handler.py      # Análises de texto (~120 linhas)
│   │       ├── image_handler.py               # Extração de imagens (~60 linhas)
│   │       ├── resume_handler.py              # Resumos com LLM (~110 linhas)
│   │       └── final_resume_handler.py        # Relatório completo (~130 linhas)
│   │
│   ├── llm/
│   │   ├── __init__.py         # Inicialização do pacote LLM
│   │   ├── model_loader.py    # Carregamento do modelo Qwen 3B e tokenizer
│   │   └── summarizer.py       # Geração de resumos com Map-Reduce
│   │
│   ├── pdf/
│   │   ├── __init__.py         # Inicialização do pacote PDF
│   │   ├── best_words.py       # Cálculo de frequência de palavras
│   │   ├── clean.py            # Limpeza e normalização de texto
│   │   ├── extractor.py        # Extração de texto e metadados do PDF
│   │   ├── headers.py          # Detecção de estrutura e cabeçalhos
│   │   ├── image.py            # Extração de imagens do PDF
│   │   ├── models.py           # Classes de dados (dataclasses/Pydantic)
│   │   └── stop_words.py       # Lista de stop words para análise
│   │
│   └── utils/
│       ├── __init__.py         # Inicialização do pacote Utils
│       ├── image_config.py     # Configurações para filtros de imagem
│       └── image_save.py       # Funções para salvar imagens extraídas
│
├── logs/                        # Logs da aplicação (gerado automaticamente)
└── README.md                    # Este arquivo
```

## 🛠️ Desativando o ambiente virtual

Quando terminar de usar a aplicação:

```bash
deactivate
```

## 📝 Notas

- Certifique-se de sempre ativar o ambiente virtual antes de executar o programa
- O arquivo PDF deve existir no caminho especificado
- As imagens extraídas serão salvas no diretório especificado (padrão: `./extracted_images`)
- O relatório final será gerado em formato Markdown
- Logs detalhados são salvos automaticamente em `./logs/app.log`

## ⚙️ Funcionalidades técnicas

### Geração de resumos com LLM

O sistema utiliza um modelo de linguagem local (LLM) para gerar resumos inteligentes:

- **Modelo**: Qwen 3B (configurável)
- **Chunking automático**: Textos grandes são divididos automaticamente em chunks processáveis
- **Consolidação**: Múltiplos resumos são consolidados em um resumo final coerente
- **Limites de token**: Sistema verifica automaticamente se o texto cabe na janela de contexto
- **Parâmetros otimizados**: Temperature 0.3, top_k 40, top_p 0.9 para resumos consistentes

### 🗺️ Arquitetura Map-Reduce para Resumos

O sistema implementa uma estratégia **Map-Reduce** para processar documentos que excedem o limite de tokens do modelo:

#### **Fase MAP (Divisão e Resumo)**
1. **Detecção automática**: O sistema verifica se o texto excede `model_max_length` (padrão: 32.768 tokens)
2. **Chunking inteligente**: Divide o texto em chunks de até 28.000 tokens cada
3. **Processamento paralelo**: Cada chunk é resumido independentemente pelo LLM
4. **Preservação de contexto**: Mantém a coerência semântica dentro de cada chunk

#### **Fase REDUCE (Consolidação)**
1. **Agregação**: Combina todos os resumos individuais dos chunks
2. **Re-sumarização**: Gera um único resumo coerente a partir dos resumos parciais
3. **Síntese final**: Produz um documento consolidado que captura a essência do texto original

#### **Fluxo de processamento**

```
Texto Grande (> 32k tokens)
        ↓
    Chunking
        ↓
   ┌────┴────┬────────┬────────┐
   ↓         ↓        ↓        ↓
Chunk 1  Chunk 2  Chunk 3  Chunk N   ← MAP
   ↓         ↓        ↓        ↓
Resumo 1 Resumo 2 Resumo 3 Resumo N
   └────┬────┴────────┴────────┘
        ↓
  Consolidação                        ← REDUCE
        ↓
  Resumo Final
```

### 🤖 Modelo Qwen 3B

**Características do modelo:**

- **Desenvolvedor**: Alibaba Cloud
- **Tamanho**: 3 bilhões de parâmetros
- **Contexto**: Suporta até 32.768 tokens
- **Especialização**: Otimizado para textos em português e múltiplos idiomas
- **Performance**: Equilibra qualidade e velocidade em hardware consumer

**Parâmetros de geração:**

```python
{
    "max_new_tokens": 512,        # Tamanho máximo do resumo
    "temperature": 0.3,           # Baixa aleatoriedade (mais determinístico)
    "top_k": 40,                  # Considera top 40 tokens mais prováveis
    "top_p": 0.9,                 # Nucleus sampling (90% probabilidade acumulada)
    "repetition_penalty": 1.1,    # Penaliza repetições
    "do_sample": True             # Habilita amostragem probabilística
}
```

**Por que Qwen 3B?**

- ✅ Roda localmente sem necessidade de GPU de alto desempenho
- ✅ Boa compreensão de português brasileiro
- ✅ Janela de contexto generosa (32k tokens)
- ✅ Balance ideal entre velocidade e qualidade
- ✅ Suporte a chat templates para prompts estruturados

## 📄 Licença

GNU


