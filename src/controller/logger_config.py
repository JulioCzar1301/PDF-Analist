"""
src/controller/logger_config.py

Configuração centralizada do sistema de logging.
"""

import logging
import pathlib
from pathlib import Path

directory_log = Path(__file__).resolve().parents[2]/"logs"

def setup_logging(
    log_dir: str = directory_log,
    log_file: str = "app.log",
    console_level: int = logging.INFO,
    file_level: int = logging.DEBUG
) -> logging.Logger:
    """
    Configura o sistema de logging com arquivo e console.
    
    Args:
        log_dir: Diretório onde os logs serão salvos.
        log_file: Nome do arquivo de log.
        console_level: Nível mínimo de log para o console.
        file_level: Nível mínimo de log para o arquivo.
    
    Returns:
        Logger configurado.
    """
    
    # Criar diretório de logs se não existir
    log_path = pathlib.Path(log_dir)
    log_path.mkdir(exist_ok=True)
    
    # Caminho completo do arquivo de log
    log_file_path = log_path / log_file
    
    # Configurar formato do log
    log_format = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para arquivo (logs detalhados)
    file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
    file_handler.setLevel(file_level)
    file_handler.setFormatter(log_format)
    
    # Configurar logger raiz
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    
    # Remover handlers existentes para evitar duplicação
    root_logger.handlers.clear()
    
    # Adicionar handlers
    root_logger.addHandler(file_handler)
    
    # Log inicial
    root_logger.info("=" * 80)
    root_logger.info(f"Sistema de logging inicializado: {log_file_path}")
    root_logger.info("=" * 80)
    
    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    Obtém um logger com o nome especificado.
    
    Args:
        name: Nome do logger (geralmente __name__ do módulo).
    
    Returns:
        Logger configurado.
    """
    return logging.getLogger(name)