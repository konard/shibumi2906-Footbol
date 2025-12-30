"""
Валидация настроек и проверка конфигурации.
"""
import sys
from typing import List, Tuple
from src.utils.logger import setup_logger

logger = setup_logger("validator")


class ValidationError(Exception):
    """Исключение для ошибок валидации."""
    pass


def validate_settings() -> Tuple[bool, List[str]]:
    """
    Валидация настроек игры.
    
    Returns:
        Кортеж (успешно ли, список ошибок)
    """
    errors: List[str] = []
    
    try:
        import settings
        
        # Проверка размеров экрана
        if settings.SCREEN_WIDTH < 800 or settings.SCREEN_HEIGHT < 600:
            errors.append(f"Размеры экрана слишком малы: {settings.SCREEN_WIDTH}x{settings.SCREEN_HEIGHT}")
        
        if settings.SCREEN_WIDTH > 3840 or settings.SCREEN_HEIGHT > 2160:
            errors.append(f"Размеры экрана слишком велики: {settings.SCREEN_WIDTH}x{settings.SCREEN_HEIGHT}")
        
        # Проверка физических параметров
        if settings.FRICTION <= 0 or settings.FRICTION >= 1:
            errors.append(f"Коэффициент трения должен быть между 0 и 1: {settings.FRICTION}")
        
        if settings.PLAYER_ACCEL <= 0:
            errors.append(f"Ускорение игрока должно быть положительным: {settings.PLAYER_ACCEL}")
        
        if settings.PLAYER_MAX_SPEED <= 0:
            errors.append(f"Максимальная скорость игрока должна быть положительной: {settings.PLAYER_MAX_SPEED}")
        
        if settings.BALL_MAX_SPEED <= 0:
            errors.append(f"Максимальная скорость мяча должна быть положительной: {settings.BALL_MAX_SPEED}")
        
        if settings.KICK_POWER <= 0:
            errors.append(f"Сила удара должна быть положительной: {settings.KICK_POWER}")
        
        if settings.KICK_RADIUS <= 0:
            errors.append(f"Радиус удара должен быть положительным: {settings.KICK_RADIUS}")
        
        # Проверка размеров объектов
        if settings.PLAYER_RADIUS <= 0:
            errors.append(f"Радиус игрока должен быть положительным: {settings.PLAYER_RADIUS}")
        
        if settings.BALL_RADIUS <= 0:
            errors.append(f"Радиус мяча должен быть положительным: {settings.BALL_RADIUS}")
        
        if settings.BALL_RADIUS >= settings.PLAYER_RADIUS:
            errors.append(f"Радиус мяча должен быть меньше радиуса игрока")
        
        # Проверка FPS
        if settings.FPS < 30 or settings.FPS > 240:
            errors.append(f"FPS должен быть между 30 и 240: {settings.FPS}")
        
        # Проверка времени игры
        if settings.GAME_DURATION <= 0:
            errors.append(f"Длительность игры должна быть положительной: {settings.GAME_DURATION}")
        
        if len(errors) > 0:
            logger.error("Обнаружены ошибки в настройках:")
            for error in errors:
                logger.error(f"  - {error}")
            return False, errors
        
        logger.info("Настройки валидированы успешно")
        return True, []
        
    except ImportError as e:
        error_msg = f"Не удалось импортировать settings: {e}"
        logger.error(error_msg)
        errors.append(error_msg)
        return False, errors
    except Exception as e:
        error_msg = f"Неожиданная ошибка при валидации: {e}"
        logger.error(error_msg)
        errors.append(error_msg)
        return False, errors


def check_dependencies() -> Tuple[bool, List[str]]:
    """
    Проверка установленных зависимостей.
    
    Returns:
        Кортеж (успешно ли, список ошибок)
    """
    errors: List[str] = []
    required_modules = {
        'pygame': 'pygame-ce',
        'sys': None,  # Встроенный модуль
    }
    
    for module_name, package_name in required_modules.items():
        try:
            __import__(module_name)
            logger.debug(f"Модуль {module_name} найден")
        except ImportError:
            error_msg = f"Модуль {module_name} не найден"
            if package_name:
                error_msg += f". Установите: pip install {package_name}"
            errors.append(error_msg)
            logger.error(error_msg)
    
    if len(errors) > 0:
        return False, errors
    
    logger.info("Все зависимости установлены")
    return True, []


def check_python_version() -> bool:
    """
    Проверка версии Python.
    
    Returns:
        True, если версия подходит
    """
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 12):
        logger.warning(
            f"Рекомендуется Python 3.12+, текущая версия: {version.major}.{version.minor}.{version.micro}"
        )
        return False
    
    logger.info(f"Версия Python: {version.major}.{version.minor}.{version.micro}")
    return True

