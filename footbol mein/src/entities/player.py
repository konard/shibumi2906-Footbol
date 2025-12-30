"""
Класс игрока с управлением и ударом.
"""
import pygame
from pygame import Vector2
from src.entities.base import Entity
from src.entities.ball import Ball
import settings


class Player(Entity):
    """Игрок с управлением WASD и ударом по мячу."""
    
    def __init__(self, pos: Vector2, color: tuple[int, int, int] = settings.BLUE) -> None:
        """
        Инициализация игрока.
        
        Args:
            pos: Начальная позиция
            color: Цвет игрока
        """
        super().__init__(pos, settings.PLAYER_RADIUS, color)
        self.mass = 1.0
        self.kick_radius = settings.KICK_RADIUS
        self.kick_power = settings.KICK_POWER
    
    def handle_input(self, keys: pygame.key.ScancodeWrapper) -> None:
        """
        Обработка ввода с клавиатуры.
        
        Args:
            keys: Состояние клавиш
        """
        direction = Vector2(0, 0)
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            direction.y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            direction.y += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            direction.x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            direction.x += 1
        
        # Нормализуем направление
        if direction.length() > 0:
            direction.normalize_ip()
            self.vel += direction * settings.PLAYER_ACCEL
        else:
            # Трение для игрока
            self.vel *= 0.9
        
        # Ограничиваем максимальную скорость
        if self.vel.length() > settings.PLAYER_MAX_SPEED:
            self.vel.scale_to_length(settings.PLAYER_MAX_SPEED)
    
    def kick(self, ball: Ball) -> bool:
        """
        Удар по мячу, если он в зоне действия.
        
        Args:
            ball: Мяч для удара
        
        Returns:
            True, если удар был выполнен
        """
        dist = self.pos.distance_to(ball.pos)
        if dist < self.kick_radius:
            # Направление от игрока к мячу
            direction = (ball.pos - self.pos)
            if direction.length() > 0:
                direction.normalize_ip()
                # Применяем силу удара
                ball.apply_force(direction * self.kick_power)
                return True
        return False
    
    def get_direction(self) -> Vector2:
        """
        Возвращает направление взгляда игрока (направление движения).
        
        Returns:
            Нормализованный вектор направления
        """
        if self.vel.length() > 0.1:
            return self.vel.normalize()
        return Vector2(1, 0)  # По умолчанию смотрим вправо
    
    def draw(self, surface: pygame.Surface) -> None:
        """
        Отрисовка игрока с индикатором направления.
        
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
        # Индикатор направления
        direction = self.get_direction()
        end_pos = self.pos + direction * (self.radius + 5)
        pygame.draw.line(
            surface,
            settings.WHITE,
            (int(self.pos.x), int(self.pos.y)),
            (int(end_pos.x), int(end_pos.y)),
            2
        )



