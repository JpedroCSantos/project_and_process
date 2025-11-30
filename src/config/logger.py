import os
import sys
from loguru import logger

def configure_logging(env: str | None = None) -> None:
    env = (env or os.getenv("APP_ENV") or os.getenv("ENV") or "DEV").upper()
    log_level = os.getenv("LOG_LEVEL", "DEBUG").upper()
    os.makedirs("logs", exist_ok=True)

    logger.remove()
    logger.add(
        sys.stderr,
        level=log_level,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | {level: <8} | {message}",
    )

    logger.add(
        "logs/app.log",
        level=log_level,
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message}",
        rotation="10 MB",     
        retention="7 days",   
        enqueue=False,        
        backtrace=False,
        diagnose=False,
    )

def get_bound_logger(**context):
    """
    Cria e retorna uma nova instância de logger com contexto vinculado (Log Estruturado).

    Esta função utiliza o método `.bind()` do Loguru para criar um logger "filho"
    que anexa automaticamente os argumentos fornecidos a todas as mensagens de log
    disparadas por ele. Isso é essencial para rastreabilidade, permitindo filtrar
    logs por ID de execução, nome de arquivo, usuário, etc.

    Args:
        **context: Argumentos nomeados (kwargs) arbitrários que serão adicionados
                   ao dicionário 'extra' de cada registro de log.

    Returns:
        loguru.Logger: Uma nova instância do logger configurada com o contexto.
    """
    return logger.bind(**context)
    