"""
Класс ворот для определения голов.
"""
import pygame
from pygame import Vector2
from src.entities.ball import Ball
import settings


class Goal:
    """Ворота с триггером для определения голов."""
    
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        side: str = "left"
    ) -> None:
        """
        Инициализация ворот.
        
        Args:
            x: Позиция X
            y: Позиция Y (верхний край)
            width: Ширина ворот
            height: Высота ворот (глубина)
            side: Сторона ("left" или "right")
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.side = side
        self.color = settings.WHITE
    
    def get_rect(self) -> pygame.Rect:
        """Возвращает прямоугольник ворот."""
        if self.side == "left":
            return pygame.Rect(
                int(self.x),
                int(self.y),
                int(self.height),
                int(self.width)
            )
        else:  # right
            return pygame.Rect(
                int(self.x - self.height),
                int(self.y),
                int(self.height),
                int(self.width)
            )
    
    def check_goal(self, ball: Ball) -> bool:
        """
        Проверяет, забит ли гол.
        
        Args:
            ball: Мяч для проверки
        
        Returns:
            True, если мяч пересек линию ворот
        """
        ball_x = ball.pos.x
        ball_y = ball.pos.y
        
        if self.side == "left":
            # Левые ворота: мяч должен быть слева от линии ворот
            if (ball_x < self.x + self.height and
                self.y <= ball_y <= self.y + self.width):
                return True
        else:  # right
            # Правые ворота: мяч должен быть справа от линии ворот
            if (ball_x > self.x - self.height and
                self.y <= ball_y <= self.y + self.width):
                return True
        
        return False
    
    def draw(self, surface: pygame.Surface) -> None:
        """
        Отрисовка ворот.
        
        Args:
            surface: Поверхность для отрисовки
        """
        rect = self.get_rect()
        pygame.draw.rect(surface, self.color, rect, 3)
        
        # Сетка ворот (опционально)
        if self.side == "left":
            # Вертикальные линии
            for i in range(3):
                x = self.x + self.height * (i + 1) / 4
                pygame.draw.line(
                    surface,
                    self.color,
                    (int(x), int(self.y)),
                    (int(x), int(self.y + self.width)),
                    1
                )
            # Горизонтальные линии
            for i in range(3):
                y = self.y + self.width * (i + 1) / 4
                pygame.draw.line(
                    surface,
                    self.color,
                    (int(self.x), int(y)),
                    (int(self.x + self.height), int(y)),
                    1
                )
        else:  # right
            # Вертикальные линии
            for i in range(3):
                x = self.x - self.height * (i + 1) / 4
                pygame.draw.line(
                    surface,
                    self.color,
                    (int(x), int(self.y)),
                    (int(x), int(self.y + self.width)),
                    1
                )
            # Горизонтальные линии
            for i in range(3):
                y = self.y + self.width * (i + 1) / 4
                pygame.draw.line(
                    surface,
                    self.color,
                    (int(self.x - self.height), int(y)),
                    (int(self.x), int(y)),
                    1
                )



