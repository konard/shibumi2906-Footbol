"""
Пользовательский интерфейс: счет, таймер, меню.
"""
import pygame
import settings


class UI:
    """Класс для отрисовки интерфейса."""
    
    def __init__(self) -> None:
        """Инициализация UI."""
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
    
    def draw_score(
        self,
        surface: pygame.Surface,
        player_score: int,
        ai_score: int
    ) -> None:
        """
        Отрисовка счета.
        
        Args:
            surface: Поверхность для отрисовки
            player_score: Счет игрока
            ai_score: Счет ИИ
        """
        score_text = f"{player_score} - {ai_score}"
        text_surface = self.font_medium.render(score_text, True, settings.WHITE)
        text_rect = text_surface.get_rect(center=(settings.SCREEN_WIDTH // 2, 30))
        surface.blit(text_surface, text_rect)
    
    def draw_timer(
        self,
        surface: pygame.Surface,
        time_remaining: int,
        ai_difficulty: int = 1
    ) -> None:
        """
        Отрисовка таймера и уровня сложности.
        
        Args:
            surface: Поверхность для отрисовки
            time_remaining: Оставшееся время в секундах
            ai_difficulty: Уровень сложности ИИ
        """
        minutes = time_remaining // 60
        seconds = time_remaining % 60
        timer_text = f"{minutes:02d}:{seconds:02d}"
        text_surface = self.font_small.render(timer_text, True, settings.WHITE)
        text_rect = text_surface.get_rect(center=(settings.SCREEN_WIDTH // 2, 70))
        surface.blit(text_surface, text_rect)
        
        # Отображение уровня сложности
        difficulty_text = f"Уровень: {'Легкий' if ai_difficulty == 1 else 'Сложный'}"
        diff_surface = self.font_small.render(difficulty_text, True, settings.YELLOW)
        diff_rect = diff_surface.get_rect(center=(settings.SCREEN_WIDTH - 150, 30))
        surface.blit(diff_surface, diff_rect)
    
    def draw_menu(self, surface: pygame.Surface, ai_difficulty: int = 1) -> None:
        """
        Отрисовка стартового меню.
        
        Args:
            surface: Поверхность для отрисовки
            ai_difficulty: Уровень сложности ИИ (1 - легкий, 2 - сложный)
        """
        # Заголовок
        title = self.font_large.render("FOOTBALL GAME", True, settings.WHITE)
        title_rect = title.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2 - 150))
        surface.blit(title, title_rect)
        
        # Уровень сложности
        difficulty_text = f"Уровень сложности: {'Легкий' if ai_difficulty == 1 else 'Сложный'}"
        diff_surface = self.font_medium.render(difficulty_text, True, settings.YELLOW)
        diff_rect = diff_surface.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2 - 80))
        surface.blit(diff_surface, diff_rect)
        
        # Инструкции
        instructions = [
            "WASD или стрелки - движение",
            "SPACE - удар по мячу",
            "1 - Легкий уровень (бот на своей половине)",
            "2 - Сложный уровень (бот по всему полю)",
            "ENTER - начать игру"
        ]
        
        y_offset = settings.SCREEN_HEIGHT // 2 - 20
        for instruction in instructions:
            text = self.font_small.render(instruction, True, settings.WHITE)
            text_rect = text.get_rect(center=(settings.SCREEN_WIDTH // 2, y_offset))
            surface.blit(text, text_rect)
            y_offset += 35
    
    def draw_goal_celebration(
        self,
        surface: pygame.Surface,
        scorer: str
    ) -> None:
        """
        Отрисовка анимации гола.
        
        Args:
            surface: Поверхность для отрисовки
            scorer: Кто забил ("Player" или "AI")
        """
        # Полупрозрачный фон
        overlay = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(settings.BLACK)
        surface.blit(overlay, (0, 0))
        
        # Текст гола
        goal_text = f"GOAL! {scorer} SCORES!"
        text_surface = self.font_large.render(goal_text, True, settings.YELLOW)
        text_rect = text_surface.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2))
        surface.blit(text_surface, text_rect)
    
    def draw_gameover(
        self,
        surface: pygame.Surface,
        player_score: int,
        ai_score: int
    ) -> None:
        """
        Отрисовка экрана окончания игры.
        
        Args:
            surface: Поверхность для отрисовки
            player_score: Счет игрока
            ai_score: Счет ИИ
        """
        # Полупрозрачный фон
        overlay = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(settings.BLACK)
        surface.blit(overlay, (0, 0))
        
        # Результат
        if player_score > ai_score:
            result_text = "YOU WIN!"
            color = settings.GREEN
        elif ai_score > player_score:
            result_text = "YOU LOSE!"
            color = settings.RED
        else:
            result_text = "DRAW!"
            color = settings.YELLOW
        
        result_surface = self.font_large.render(result_text, True, color)
        result_rect = result_surface.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2 - 100))
        surface.blit(result_surface, result_rect)
        
        # Финальный счет
        score_text = f"Final Score: {player_score} - {ai_score}"
        score_surface = self.font_medium.render(score_text, True, settings.WHITE)
        score_rect = score_surface.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2))
        surface.blit(score_surface, score_rect)
        
        # Инструкция
        restart_text = "Press R to restart or ESC to quit"
        restart_surface = self.font_small.render(restart_text, True, settings.WHITE)
        restart_rect = restart_surface.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2 + 100))
        surface.blit(restart_surface, restart_rect)

