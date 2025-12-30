"""
Менеджер состояний игры.
"""
from enum import Enum
from typing import Optional
import pygame
from pygame import Vector2
from src.entities.player import Player
from src.entities.ball import Ball
from src.entities.goal import Goal
from src.ai.bot import Bot
from src.physics.collisions import (
    check_circle_circle_collision,
    resolve_circle_circle_collision,
    handle_ball_wall_collision,
    handle_player_wall_collision
)
from src.ui.interface import UI
from src.utils.errors import EntityError, PhysicsError, AIError, RenderError
import settings


class GameState(Enum):
    """Состояния игры."""
    MENU = "menu"
    PLAYING = "playing"
    GOAL_CELEBRATION = "goal_celebration"
    GAMEOVER = "gameover"


class GameStateManager:
    """Менеджер состояний игры."""
    
    def __init__(self) -> None:
        """Инициализация менеджера."""
        self.state = GameState.MENU
        self.ui = UI()
        
        # Игровые объекты
        self.player: Optional[Player] = None
        self.bot: Optional[Bot] = None
        self.ball: Optional[Ball] = None
        self.left_goal: Optional[Goal] = None
        self.right_goal: Optional[Goal] = None
        
        # Счет
        self.player_score = 0
        self.ai_score = 0
        
        # Таймер
        self.game_time = settings.GAME_DURATION
        self.last_time_update = 0
        
        # Гол
        self.goal_timer = 0
        self.goal_scorer: Optional[str] = None
        
        # Уровень сложности ИИ
        self.ai_difficulty = settings.AI_DIFFICULTY_EASY  # По умолчанию легкий
    
    def reset_game(self) -> None:
        """
        Сброс игры к начальному состоянию.
        
        Raises:
            EntityError: Если не удалось создать игровые объекты
        """
        try:
            # Создаем игровые объекты
            player_pos = Vector2(settings.SCREEN_WIDTH * 0.25, settings.SCREEN_HEIGHT // 2)
            bot_pos = Vector2(settings.SCREEN_WIDTH * 0.75, settings.SCREEN_HEIGHT // 2)
            ball_pos = Vector2(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2)
            
            self.player = Player(player_pos)
            self.bot = Bot(bot_pos)
            self.bot.set_difficulty(self.ai_difficulty)  # Устанавливаем уровень сложности
            self.ball = Ball(ball_pos)
            
            # Проверяем, что объекты созданы
            if not all([self.player, self.bot, self.ball]):
                raise EntityError("Не удалось создать все игровые объекты")
            
            # Создаем ворота
            try:
                self.left_goal = Goal(
                    settings.GOAL_LEFT_X,
                    settings.GOAL_LEFT_Y,
                    settings.GOAL_WIDTH,
                    settings.GOAL_HEIGHT,
                    "left"
                )
                self.right_goal = Goal(
                    settings.GOAL_RIGHT_X,
                    settings.GOAL_RIGHT_Y,
                    settings.GOAL_WIDTH,
                    settings.GOAL_HEIGHT,
                    "right"
                )
            except Exception as e:
                raise EntityError("Не удалось создать ворота", str(e)) from e
            
            # Сбрасываем счет и таймер
            self.player_score = 0
            self.ai_score = 0
            self.game_time = settings.GAME_DURATION
            self.last_time_update = pygame.time.get_ticks()
            self.state = GameState.PLAYING
            
        except Exception as e:
            if isinstance(e, EntityError):
                raise
            raise EntityError("Ошибка при сбросе игры", str(e)) from e
    
    def handle_input(self, keys: pygame.key.ScancodeWrapper) -> None:
        """
        Обработка ввода в зависимости от состояния.
        
        Args:
            keys: Состояние клавиш
        """
        if self.state == GameState.MENU:
            # Выбор уровня сложности
            if keys[pygame.K_1]:
                self.ai_difficulty = settings.AI_DIFFICULTY_EASY
            elif keys[pygame.K_2]:
                self.ai_difficulty = settings.AI_DIFFICULTY_HARD
            
            if keys[pygame.K_RETURN] or keys[pygame.K_KP_ENTER]:
                self.reset_game()
        elif self.state == GameState.PLAYING:
            if self.player:
                self.player.handle_input(keys)
                if keys[pygame.K_SPACE]:
                    if self.ball:
                        self.player.kick(self.ball)
        elif self.state == GameState.GAMEOVER:
            if keys[pygame.K_r]:
                self.reset_game()
    
    def update(self, dt: float) -> None:
        """
        Обновление логики игры.
        
        Args:
            dt: Дельта времени
        
        Raises:
            EntityError: Если игровые объекты не инициализированы
            PhysicsError: Если произошла ошибка физики
            AIError: Если произошла ошибка ИИ
        """
        current_time = pygame.time.get_ticks()
        
        if self.state == GameState.PLAYING:
            if not all([self.player, self.bot, self.ball]):
                raise EntityError(
                    "Игровые объекты не инициализированы",
                    f"player={self.player is not None}, bot={self.bot is not None}, ball={self.ball is not None}"
                )
            
            # Обновляем таймер
            if current_time - self.last_time_update >= 1000:  # Каждую секунду
                self.game_time -= 1
                self.last_time_update = current_time
                
                if self.game_time <= 0:
                    self.state = GameState.GAMEOVER
                    return
            
            # Обновляем ИИ
            try:
                self.bot.update_ai(
                    self.ball,
                    self.player,
                    settings.GOAL_LEFT_X,
                    settings.GOAL_RIGHT_X
                )
            except Exception as e:
                raise AIError("Ошибка обновления ИИ", str(e)) from e
            
            # Обновляем позиции
            try:
                self.player.update(dt)
                self.bot.update(dt)
                self.ball.update(dt)
            except Exception as e:
                raise EntityError("Ошибка обновления позиций объектов", str(e)) from e
            
            # Обрабатываем столкновения со стенами
            try:
                handle_player_wall_collision(self.player)
                handle_player_wall_collision(self.bot)
                handle_ball_wall_collision(self.ball)
            except Exception as e:
                raise PhysicsError("Ошибка обработки столкновений со стенами", str(e)) from e
            
            # Обрабатываем столкновения между объектами
            try:
                if check_circle_circle_collision(self.player, self.ball):
                    resolve_circle_circle_collision(self.player, self.ball)
                
                if check_circle_circle_collision(self.bot, self.ball):
                    resolve_circle_circle_collision(self.bot, self.ball)
                
                if check_circle_circle_collision(self.player, self.bot):
                    resolve_circle_circle_collision(self.player, self.bot)
            except Exception as e:
                raise PhysicsError("Ошибка обработки столкновений между объектами", str(e)) from e
            
            # Проверяем голы
            if self.left_goal and self.left_goal.check_goal(self.ball):
                self.ai_score += 1
                self.goal_scorer = "AI"
                self.state = GameState.GOAL_CELEBRATION
                self.goal_timer = current_time
                self._reset_after_goal()
            
            elif self.right_goal and self.right_goal.check_goal(self.ball):
                self.player_score += 1
                self.goal_scorer = "Player"
                self.state = GameState.GOAL_CELEBRATION
                self.goal_timer = current_time
                self._reset_after_goal()
        
        elif self.state == GameState.GOAL_CELEBRATION:
            # Пауза после гола
            if current_time - self.goal_timer >= settings.GOAL_CELEBRATION_TIME:
                self.state = GameState.PLAYING
    
    def _reset_after_goal(self) -> None:
        """Сброс позиций после гола."""
        if self.player and self.bot and self.ball:
            self.player.pos = Vector2(settings.SCREEN_WIDTH * 0.25, settings.SCREEN_HEIGHT // 2)
            self.player.vel = Vector2(0, 0)
            self.bot.pos = Vector2(settings.SCREEN_WIDTH * 0.75, settings.SCREEN_HEIGHT // 2)
            self.bot.vel = Vector2(0, 0)
            self.ball.pos = Vector2(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2)
            self.ball.vel = Vector2(0, 0)
    
    def draw(self, surface: pygame.Surface) -> None:
        """
        Отрисовка игры.
        
        Args:
            surface: Поверхность для отрисовки
        
        Raises:
            RenderError: Если произошла ошибка отрисовки
        """
        try:
            if self.state == GameState.MENU:
                self._draw_menu(surface)
            elif self.state == GameState.PLAYING:
                self._draw_playing(surface)
            elif self.state == GameState.GOAL_CELEBRATION:
                self._draw_playing(surface)
                if self.goal_scorer:
                    self.ui.draw_goal_celebration(surface, self.goal_scorer)
            elif self.state == GameState.GAMEOVER:
                self._draw_playing(surface)
                self.ui.draw_gameover(surface, self.player_score, self.ai_score)
        except Exception as e:
            raise RenderError("Ошибка отрисовки игры", str(e)) from e
    
    def _draw_menu(self, surface: pygame.Surface) -> None:
        """Отрисовка меню."""
        surface.fill(settings.DARK_GREEN)
        self.ui.draw_menu(surface, self.ai_difficulty)
    
    def _draw_playing(self, surface: pygame.Surface) -> None:
        """Отрисовка игрового процесса."""
        # Фон поля
        surface.fill(settings.DARK_GREEN)
        
        # Рисуем поле
        pitch_rect = pygame.Rect(
            settings.PITCH_LEFT,
            settings.PITCH_TOP,
            settings.PITCH_WIDTH,
            settings.PITCH_HEIGHT
        )
        pygame.draw.rect(surface, settings.GREEN, pitch_rect)
        pygame.draw.rect(surface, settings.WHITE, pitch_rect, 3)
        
        # Центральная линия
        pygame.draw.line(
            surface,
            settings.WHITE,
            (settings.SCREEN_WIDTH // 2, settings.PITCH_TOP),
            (settings.SCREEN_WIDTH // 2, settings.PITCH_BOTTOM),
            2
        )
        
        # Центральный круг
        pygame.draw.circle(
            surface,
            settings.WHITE,
            (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2),
            80,
            2
        )
        
        # Ворота
        if self.left_goal:
            self.left_goal.draw(surface)
        if self.right_goal:
            self.right_goal.draw(surface)
        
        # Игровые объекты
        if self.player:
            self.player.draw(surface)
        if self.bot:
            self.bot.draw(surface)
        if self.ball:
            self.ball.draw(surface)
        
        # UI
        self.ui.draw_score(surface, self.player_score, self.ai_score)
        self.ui.draw_timer(surface, self.game_time, self.ai_difficulty)

