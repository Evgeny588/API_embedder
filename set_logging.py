import sys
from loguru import logger

def setup_logging(name: str):
    """
    Настройка логгера loguru.
    Аргумент name используется для обозначения модуля в логах.
    """
    logger.remove()

    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO",
        colorize=True
    )

    logger.add(
        "logs/app_logs.log",
        rotation="10 MB", 
        retention="7 days",
        compression="zip",
        level="DEBUG"
    )

    return logger.bind(name=name)