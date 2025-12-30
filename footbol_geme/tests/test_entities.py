"""
Тесты для игровых сущностей.
"""
import pytest
import pygame
from pygame import Vector2
from src.entities.base import Entity
from src.entities.ball import Ball
from src.entities.player import Player
import settings


class TestEntity:
    """Тесты для базового класса Entity."""
    
    def test_entity_creation(self):
        """Тест создания сущности."""
        entity = Entity(Vector2(100, 100), 20, (255, 0, 0))
        assert entity.pos == Vector2(100, 100)
        assert entity.radius == 20
        assert entity.color == (255, 0, 0)
        assert entity.vel == Vector2(0, 0)
        assert entity.mass == 1.0
    
    def test_entity_update(self):
        """Тест обновления позиции сущности."""
        entity = Entity(Vector2(100, 100), 20)
        entity.vel = Vector2(5, 3)
        entity.update(1.0)
        assert entity.pos == Vector2(105, 103)
    
    def test_entity_apply_force(self):
        """Тест применения силы к сущности."""
        entity = Entity(Vector2(100, 100), 20)
        entity.mass = 2.0
        entity.apply_force(Vector2(10, 0))
        assert entity.vel == Vector2(5, 0)  # 10 / 2 = 5
    
    def test_entity_get_rect(self):
        """Тест получения прямоугольника для отрисовки."""
        entity = Entity(Vector2(100, 100), 20)
        rect = entity.get_rect()
        assert rect.x == 80  # 100 - 20
        assert rect.y == 80  # 100 - 20
        assert rect.width == 40  # 20 * 2
        assert rect.height == 40  # 20 * 2


class TestBall:
    """Тесты для класса Ball."""
    
    def test_ball_creation(self):
        """Тест создания мяча."""
        ball = Ball(Vector2(200, 200))
        assert ball.radius == settings.BALL_RADIUS
        assert ball.mass == 0.5
        assert ball.color == settings.WHITE
    
    def test_ball_friction(self):
        """Тест применения трения к мячу."""
        ball = Ball(Vector2(100, 100))
        ball.vel = Vector2(10, 10)
        initial_speed = ball.vel.length()
        ball.update(1.0)
        new_speed = ball.vel.length()
        assert new_speed < initial_speed
        assert new_speed == pytest.approx(initial_speed * settings.FRICTION, rel=0.01)
    
    def test_ball_max_speed_limit(self):
        """Тест ограничения максимальной скорости мяча."""
        ball = Ball(Vector2(100, 100))
        ball.vel = Vector2(100, 100)  # Очень большая скорость
        ball.update(1.0)
        # Используем pytest.approx для учета погрешности вычислений с плавающей точкой
        assert ball.vel.length() <= settings.BALL_MAX_SPEED + 1e-10
    
    def test_ball_draw(self):
        """Тест отрисовки мяча (проверка отсутствия ошибок)."""
        pygame.init()
        surface = pygame.Surface((800, 600))
        ball = Ball(Vector2(400, 300))
        try:
            ball.draw(surface)
            assert True  # Если не было исключения, всё хорошо
        except Exception as e:
            pytest.fail(f"Ошибка при отрисовке мяча: {e}")
        finally:
            pygame.quit()


class TestPlayer:
    """Тесты для класса Player."""
    
    def test_player_creation(self):
        """Тест создания игрока."""
        player = Player(Vector2(100, 100))
        assert player.radius == settings.PLAYER_RADIUS
        assert player.kick_radius == settings.KICK_RADIUS
        assert player.kick_power == settings.KICK_POWER
    
    def test_player_handle_input(self):
        """Тест обработки ввода игрока."""
        pygame.init()
        try:
            player = Player(Vector2(100, 100))
            # Создаем мок клавиш
            class MockKeys:
                def __getitem__(self, key):
                    return key == pygame.K_w  # Нажата только W
            
            keys = MockKeys()
            player.handle_input(keys)
            # Проверяем, что скорость изменилась
            assert player.vel.y < 0  # Движение вверх
        finally:
            pygame.quit()
    
    def test_player_kick(self):
        """Тест удара игрока по мячу."""
        player = Player(Vector2(100, 100))
        ball = Ball(Vector2(120, 100))  # Мяч в зоне удара
        
        initial_vel = ball.vel.copy()
        result = player.kick(ball)
        
        assert result is True
        assert ball.vel.length() > initial_vel.length()
    
    def test_player_kick_out_of_range(self):
        """Тест удара, когда мяч вне зоны действия."""
        player = Player(Vector2(100, 100))
        ball = Ball(Vector2(500, 500))  # Мяч далеко
        
        result = player.kick(ball)
        assert result is False
    
    def test_player_max_speed_limit(self):
        """Тест ограничения максимальной скорости игрока."""
        pygame.init()
        try:
            player = Player(Vector2(100, 100))
            player.vel = Vector2(100, 100)  # Очень большая скорость
            # Создаем мок клавиш, который возвращает False для всех клавиш
            class MockKeysEmpty:
                def __getitem__(self, key):
                    return False

            keys = MockKeysEmpty()
            player.handle_input(keys)  # Пустой ввод, но трение применится
            assert player.vel.length() <= settings.PLAYER_MAX_SPEED
        finally:
            pygame.quit()
    
    def test_player_get_direction(self):
        """Тест получения направления взгляда игрока."""
        player = Player(Vector2(100, 100))
        # Без движения - направление по умолчанию
        direction = player.get_direction()
        assert direction == Vector2(1, 0)  # По умолчанию вправо
        
        # С движением
        player.vel = Vector2(0, -1)
        direction = player.get_direction()
        assert direction.y < 0  # Движение вверх
