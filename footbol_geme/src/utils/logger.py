"""
Система логирования для игры.
"""
import logging
import sys
from datetime import datetime
from pathlib import Path


def setup_logger(name: str = "football_game", level: int = logging.INFO) -> logging.Logger:
    """
    Настройка логгера для игры.
    
    Args:
        name: Имя логгера
        level: Уровень логирования
    
    Returns:
        Настроенный логгер
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Очищаем существующие обработчики
    logger.handlers.clear()
    
    # Формат логов
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Обработчик для консоли
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Обработчик для файла (опционально)
    try:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / f"game_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"Не удалось создать файл логов: {e}")
    
    return logger
