"""
Базовый класс для всех игровых сущностей.
"""
from typing import Optional
import pygame
from pygame import Vector2


class Entity:
    """Базовый класс для игровых объектов с физикой."""
    
    def __init__(
        self,
        pos: Vector2,
        radius: float,
        color: tuple[int, int, int] = (255, 255, 255)
    ) -> None:
        """
        Инициализация сущности.
        
        Args:
            pos: Начальная позиция (Vector2)
            radius: Радиус хитбокса
            color: Цвет для отрисовки
        """
        self.pos = Vector2(pos)
        self.vel = Vector2(0, 0)
        self.radius = radius
        self.color = color
        self.mass: float = 1.0
    
    def update(self, dt: float) -> None:
        """
        Обновление позиции на основе скорости.
        
        Args:
            dt: Дельта времени (обычно 1.0 для фиксированного шага)
        """
        self.pos += self.vel * dt
    
    def apply_force(self, force: Vector2) -> None:
        """
        Применение силы к сущности.
        
        Args:
            force: Вектор силы
        """
        self.vel += force / self.mass
    
    def get_rect(self) -> pygame.Rect:
        """Возвращает прямоугольник для отрисовки."""
        return pygame.Rect(
            self.pos.x - self.radius,
            self.pos.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )
    
    def draw(self, surface: pygame.Surface) -> None:
        """
        Отрисовка сущности.
        
        Args:
            surface: Поверхность для отрисовки
        """
        pygame.draw.circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), int(self.radius))



