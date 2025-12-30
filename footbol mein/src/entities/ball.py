"""
Класс мяча с физикой.
"""
import math
import pygame
from pygame import Vector2
from src.entities.base import Entity
import settings


class Ball(Entity):
    """Мяч с физикой трения и ограничением скорости."""
    
    def __init__(self, pos: Vector2) -> None:
        """
        Инициализация мяча.
        
        Args:
            pos: Начальная позиция
        """
        super().__init__(pos, settings.BALL_RADIUS, settings.WHITE)
        self.mass = 0.5
    
    def update(self, dt: float) -> None:
        """
        Обновление позиции с применением трения.
        
        Args:
            dt: Дельта времени
        """
        # Применяем трение
        self.vel *= settings.FRICTION
        
        # Ограничиваем максимальную скорость
        if self.vel.length() > settings.BALL_MAX_SPEED:
            self.vel.scale_to_length(settings.BALL_MAX_SPEED)
        
        # Обновляем позицию
        super().update(dt)
    
    def draw(self, surface: pygame.Surface) -> None:
        """
        Отрисовка мяча с обводкой.
        
        Args:
            surface: Поверхность для отрисовки
        """
        # Основной круг
        pygame.draw.circle(
            surface,
            self.color,
            (int(self.pos.x), int(self.pos.y)),
            int(self.radius)
        )
        # Обводка
        pygame.draw.circle(
            surface,
            settings.BLACK,
            (int(self.pos.x), int(self.pos.y)),
            int(self.radius),
            2
        )
        # Паттерн (пентагон для футбольного мяча)
        center = (int(self.pos.x), int(self.pos.y))
        points = []
        for i in range(5):
            angle = i * 2 * math.pi / 5 - math.pi / 2
            x = center[0] + int(self.radius * 0.6 * math.cos(angle))
            y = center[1] + int(self.radius * 0.6 * math.sin(angle))
            points.append((x, y))
        if len(points) >= 3:
            pygame.draw.polygon(surface, settings.BLACK, points, 1)

