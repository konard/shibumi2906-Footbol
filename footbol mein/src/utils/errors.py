"""
Кастомные исключения для игры.
"""
from typing import Optional


class GameError(Exception):
    """Базовое исключение для игровых ошибок."""
    
    def __init__(self, message: str, details: Optional[str] = None):
        """
        Инициализация исключения.
        
        Args:
            message: Основное сообщение об ошибке
            details: Дополнительные детали
        """
        self.message = message
        self.details = details
        super().__init__(self.message)
    
    def __str__(self) -> str:
        """Строковое представление ошибки."""
        if self.details:
            return f"{self.message}\nДетали: {self.details}"
        return self.message


class InitializationError(GameError):
    """Ошибка инициализации игры."""
    pass


class EntityError(GameError):
    """Ошибка работы с сущностями."""
    pass


class PhysicsError(GameError):
    """Ошибка физики."""
    pass


class AIError(GameError):
    """Ошибка ИИ."""
    pass


class RenderError(GameError):
    """Ошибка отрисовки."""
    pass



