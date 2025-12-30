"""
Тесты для физики столкновений.
"""
import pytest
from pygame import Vector2
from src.entities.base import Entity
from src.entities.ball import Ball
from src.entities.player import Player
from src.physics.collisions import (
    check_circle_circle_collision,
    resolve_circle_circle_collision,
    check_wall_collision,
    resolve_wall_collision,
    handle_ball_wall_collision,
    handle_player_wall_collision
)
import settings


class TestCircleCollisions:
    """Тесты для столкновений круг-круг."""
    
    def test_check_circle_circle_collision_true(self):
        """Тест обнаружения столкновения двух кругов."""
        entity1 = Entity(Vector2(100, 100), 20)
        entity2 = Entity(Vector2(115, 100), 20)  # Пересекаются
        assert check_circle_circle_collision(entity1, entity2) is True
    
    def test_check_circle_circle_collision_false(self):
        """Тест отсутствия столкновения."""
        entity1 = Entity(Vector2(100, 100), 20)
        entity2 = Entity(Vector2(200, 200), 20)  # Далеко друг от друга
        assert check_circle_circle_collision(entity1, entity2) is False
    
    def test_resolve_circle_circle_collision(self):
        """Тест разрешения столкновения."""
        entity1 = Entity(Vector2(100, 100), 20)
        entity2 = Entity(Vector2(115, 100), 20)
        entity1.vel = Vector2(5, 0)
        entity2.vel = Vector2(-5, 0)
        
        initial_vel1 = entity1.vel.copy()
        initial_vel2 = entity2.vel.copy()
        
        resolve_circle_circle_collision(entity1, entity2)
        
        # Скорости должны измениться (отскок)
        assert entity1.vel != initial_vel1 or entity2.vel != initial_vel2
    
    def test_resolve_collision_separation(self):
        """Тест разделения объектов при столкновении."""
        entity1 = Entity(Vector2(100, 100), 20)
        entity2 = Entity(Vector2(115, 100), 20)  # Пересекаются
        
        initial_dist = entity1.pos.distance_to(entity2.pos)
        resolve_circle_circle_collision(entity1, entity2)
        new_dist = entity1.pos.distance_to(entity2.pos)
        
        # После разрешения расстояние должно быть больше или равно сумме радиусов
        assert new_dist >= (entity1.radius + entity2.radius) - 1  # Небольшая погрешность


class TestWallCollisions:
    """Тесты для столкновений со стенами."""
    
    def test_check_wall_collision_left(self):
        """Тест столкновения с левой стеной."""
        entity = Entity(Vector2(settings.PITCH_LEFT - 10, 100), 20)
        collided, normal = check_wall_collision(entity)
        assert collided is True
        assert normal.x > 0  # Нормаль направлена вправо
    
    def test_check_wall_collision_right(self):
        """Тест столкновения с правой стеной."""
        entity = Entity(Vector2(settings.PITCH_RIGHT + 10, 100), 20)
        collided, normal = check_wall_collision(entity)
        assert collided is True
        assert normal.x < 0  # Нормаль направлена влево
    
    def test_check_wall_collision_top(self):
        """Тест столкновения с верхней стеной."""
        entity = Entity(Vector2(100, settings.PITCH_TOP - 10), 20)
        collided, normal = check_wall_collision(entity)
        assert collided is True
        assert normal.y > 0  # Нормаль направлена вниз
    
    def test_check_wall_collision_bottom(self):
        """Тест столкновения с нижней стеной."""
        entity = Entity(Vector2(100, settings.PITCH_BOTTOM + 10), 20)
        collided, normal = check_wall_collision(entity)
        assert collided is True
        assert normal.y < 0  # Нормаль направлена вверх
    
    def test_resolve_wall_collision_ball(self):
        """Тест разрешения столкновения мяча со стеной."""
        ball = Ball(Vector2(settings.PITCH_LEFT - 5, 100))
        ball.vel = Vector2(-10, 0)  # Движется влево
        
        initial_speed = ball.vel.length()
        resolve_wall_collision(ball)
        
        # Скорость должна отразиться и уменьшиться из-за затухания
        assert ball.vel.x > 0  # Теперь движется вправо
        assert ball.vel.length() < initial_speed * 1.1  # С учетом затухания
    
    def test_handle_ball_wall_collision(self):
        """Тест обработки столкновения мяча со стеной."""
        ball = Ball(Vector2(settings.PITCH_LEFT - 5, 100))
        ball.vel = Vector2(-5, 0)
        
        handle_ball_wall_collision(ball)
        
        # Мяч должен быть внутри поля
        assert ball.pos.x >= settings.PITCH_LEFT
    
    def test_handle_player_wall_collision(self):
        """Тест обработки столкновения игрока со стеной."""
        player = Player(Vector2(settings.PITCH_LEFT - 5, 100))
        player.vel = Vector2(-5, 0)
        
        handle_player_wall_collision(player)
        
        # Игрок должен быть внутри поля
        assert player.pos.x >= settings.PITCH_LEFT
        # Скорость в направлении стены должна быть остановлена
        assert player.vel.x >= 0
