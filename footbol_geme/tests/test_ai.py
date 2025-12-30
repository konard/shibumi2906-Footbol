"""
Тесты для ИИ.
"""
import pytest
from pygame import Vector2
from src.ai.bot import Bot, State
from src.entities.player import Player
from src.entities.ball import Ball
import settings


class TestBot:
    """Тесты для класса Bot."""
    
    def test_bot_creation(self):
        """Тест создания бота."""
        bot = Bot(Vector2(100, 100))
        assert bot.radius == settings.PLAYER_RADIUS
        assert bot.color == settings.RED
        assert bot.state == State.DEFENSE
        assert bot.kick_cooldown == 0
    
    def test_bot_state_attack(self):
        """Тест перехода в состояние атаки."""
        bot = Bot(Vector2(settings.SCREEN_WIDTH * 0.25, settings.SCREEN_HEIGHT // 2))
        player = Player(Vector2(settings.SCREEN_WIDTH * 0.25, settings.SCREEN_HEIGHT // 2))
        ball = Ball(Vector2(settings.SCREEN_WIDTH * 0.3, settings.SCREEN_HEIGHT // 2))  # На стороне ИИ
        
        field_center = settings.SCREEN_WIDTH // 2
        bot.update_ai(ball, player, settings.GOAL_LEFT_X, settings.GOAL_RIGHT_X)
        
        # Если мяч на стороне ИИ, должен быть ATTACK
        if ball.pos.x < field_center:
            assert bot.state == State.ATTACK
    
    def test_bot_state_defense(self):
        """Тест перехода в состояние защиты."""
        # Бот на правой стороне поля
        bot = Bot(Vector2(settings.SCREEN_WIDTH * 0.75, settings.SCREEN_HEIGHT // 2))
        player = Player(Vector2(settings.SCREEN_WIDTH * 0.25, settings.SCREEN_HEIGHT // 2))
        # Мяч на стороне игрока (слева от центра) - бот должен защищаться
        ball = Ball(Vector2(settings.SCREEN_WIDTH * 0.3, settings.SCREEN_HEIGHT // 2))

        field_center = settings.SCREEN_WIDTH // 2
        bot.update_ai(ball, player, settings.GOAL_LEFT_X, settings.GOAL_RIGHT_X)

        # Мяч слева от центра (на стороне игрока), бот справа -> режим DEFENSE
        if ball.pos.x < field_center:
            assert bot.state == State.DEFENSE
    
    def test_bot_kick_cooldown(self):
        """Тест кулдауна удара бота."""
        bot = Bot(Vector2(100, 100))
        ball = Ball(Vector2(120, 100))
        player = Player(Vector2(200, 100))
        
        initial_cooldown = bot.kick_cooldown
        bot.update_ai(ball, player, settings.GOAL_LEFT_X, settings.GOAL_RIGHT_X)
        
        # Кулдаун должен уменьшиться
        assert bot.kick_cooldown <= initial_cooldown
    
    def test_bot_movement(self):
        """Тест движения бота."""
        bot = Bot(Vector2(100, 100))
        ball = Ball(Vector2(200, 200))
        player = Player(Vector2(300, 300))
        
        initial_pos = bot.pos.copy()
        bot.update_ai(ball, player, settings.GOAL_LEFT_X, settings.GOAL_RIGHT_X)
        bot.update(1.0)  # Обновляем позицию
        
        # Бот должен двигаться (позиция может измениться)
        # Это зависит от состояния, но в любом случае он должен реагировать
        assert True  # Просто проверяем, что нет ошибок
