"""
Тесты для обработки ошибок.
"""
import pytest
import pygame
from pygame import Vector2
from src.utils.errors import (
    GameError,
    InitializationError,
    EntityError,
    PhysicsError,
    AIError,
    RenderError
)
from src.entities.base import Entity
from src.manager import GameStateManager


class TestCustomErrors:
    """Тесты для кастомных исключений."""
    
    def test_game_error_basic(self):
        """Тест базового исключения GameError."""
        error = GameError("Тестовая ошибка")
        assert str(error) == "Тестовая ошибка"
        assert error.message == "Тестовая ошибка"
        assert error.details is None
    
    def test_game_error_with_details(self):
        """Тест GameError с деталями."""
        error = GameError("Основная ошибка", "Детали ошибки")
        assert "Основная ошибка" in str(error)
        assert "Детали ошибки" in str(error)
        assert error.details == "Детали ошибки"
    
    def test_initialization_error(self):
        """Тест InitializationError."""
        error = InitializationError("Ошибка инициализации", "Детали")
        assert isinstance(error, GameError)
        assert error.message == "Ошибка инициализации"
    
    def test_entity_error(self):
        """Тест EntityError."""
        error = EntityError("Ошибка сущности")
        assert isinstance(error, GameError)
    
    def test_physics_error(self):
        """Тест PhysicsError."""
        error = PhysicsError("Ошибка физики")
        assert isinstance(error, GameError)
    
    def test_ai_error(self):
        """Тест AIError."""
        error = AIError("Ошибка ИИ")
        assert isinstance(error, GameError)
    
    def test_render_error(self):
        """Тест RenderError."""
        error = RenderError("Ошибка отрисовки")
        assert isinstance(error, GameError)


class TestErrorHandling:
    """Тесты для обработки ошибок в игровых компонентах."""

    def test_manager_reset_game_error(self):
        """Тест обработки ошибок при сбросе игры."""
        pygame.init()
        try:
            manager = GameStateManager()
            # Это должно работать без ошибок
            try:
                manager.reset_game()
                assert manager.player is not None
                assert manager.bot is not None
                assert manager.ball is not None
            except EntityError:
                pytest.fail("Не должно быть ошибки при нормальном сбросе игры")
        finally:
            pygame.quit()

    def test_manager_update_without_objects(self):
        """Тест обработки обновления без инициализированных объектов."""
        pygame.init()
        try:
            manager = GameStateManager()
            # Не вызываем reset_game, объекты не инициализированы

            # В состоянии MENU не должно быть ошибки
            try:
                manager.update(1.0)
            except EntityError:
                pytest.fail("Не должно быть ошибки в состоянии MENU")

            # Но если перейти в PLAYING без инициализации - должна быть ошибка
            manager.state = manager.state.__class__.PLAYING
            with pytest.raises(EntityError):
                manager.update(1.0)
        finally:
            pygame.quit()



