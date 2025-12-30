"""
Главный файл запуска игры.
"""
import sys
import traceback
# pygame импортируется после проверки зависимостей
from src.utils.logger import setup_logger
from src.utils.errors import InitializationError, GameError
import settings


def check_dependencies(logger_instance=None):
    """
    Проверка наличия необходимых зависимостей.
    
    Args:
        logger_instance: Экземпляр логгера (опционально)
    
    Returns:
        Модуль pygame
    
    Raises:
        InitializationError: Если зависимости не установлены
    """
    try:
        import pygame
        version = pygame.version.ver
        if logger_instance:
            logger_instance.info(f"pygame-ce версия: {version}")
        return pygame
    except ImportError as e:
        error_msg = (
            "pygame-ce не установлен!\n\n"
            "Для установки выполните:\n"
            "  pip install pygame-ce\n\n"
            "Или используйте:\n"
            "  pip install -r requirements.txt"
        )
        raise InitializationError(error_msg, str(e)) from e


# Глобальный логгер
logger = None
# Глобальная переменная для pygame
pygame_module = None


def main() -> None:
    """Главная функция запуска игры."""
    global logger
    logger = setup_logger()
    
    try:
        logger.info("=" * 60)
        logger.info("Запуск Football Game")
        logger.info("=" * 60)
        
        # Проверка зависимостей и импорт pygame
        global pygame_module
        logger.info("Проверка зависимостей...")
        pygame_module = check_dependencies(logger)
        pygame = pygame_module  # Локальная переменная для удобства
        
        # Импорт остальных модулей, которые используют pygame
        from src.manager import GameStateManager, GameState
        
        # Инициализация pygame
        logger.info("Инициализация pygame...")
        pygame.init()
        
        # Проверка инициализации
        if not pygame.get_init():
            raise InitializationError("Не удалось инициализировать pygame")
        
        logger.info("Создание окна игры...")
        # Создание окна
        try:
            screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
            pygame.display.set_caption("Football Game")
            logger.info(f"Окно создано: {settings.SCREEN_WIDTH}x{settings.SCREEN_HEIGHT}")
        except pygame.error as e:
            raise InitializationError(
                f"Не удалось создать окно игры ({settings.SCREEN_WIDTH}x{settings.SCREEN_HEIGHT})",
                str(e)
            ) from e
        
        clock = pygame.time.Clock()
        
        # Создание менеджера состояний
        logger.info("Инициализация игрового менеджера...")
        try:
            game_manager = GameStateManager()
            logger.info("Игровой менеджер инициализирован")
        except Exception as e:
            raise InitializationError("Не удалось инициализировать игровой менеджер", str(e)) from e
        
        logger.info("Игра запущена успешно!")
        logger.info("Главный цикл игры начат")
        
        # Главный цикл игры
        running = True
        frame_count = 0
        error_count = 0
        max_errors = 10  # Максимальное количество ошибок подряд
        
        while running:
            try:
                # Обработка событий
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        logger.info("Получен сигнал выхода")
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            if game_manager.state == GameState.PLAYING:
                                logger.info("Игра приостановлена (ESC)")
                                game_manager.state = GameState.GAMEOVER
                            else:
                                logger.info("Выход из игры (ESC)")
                                running = False
                
                # Получаем состояние клавиш
                keys = pygame.key.get_pressed()
                game_manager.handle_input(keys)
                
                # Обновление игры
                dt = 1.0  # Фиксированный шаг времени
                game_manager.update(dt)
                
                # Отрисовка
                game_manager.draw(screen)
                pygame.display.flip()
                
                # Ограничение FPS
                clock.tick(settings.FPS)
                
                frame_count += 1
                error_count = 0  # Сбрасываем счетчик ошибок при успешном кадре
                
                # Логируем каждые 1000 кадров
                if frame_count % 1000 == 0:
                    fps = clock.get_fps()
                    logger.debug(f"Кадр {frame_count}, FPS: {fps:.2f}")
            
            except GameError as e:
                error_count += 1
                logger.error(f"Игровая ошибка: {e.message}")
                if e.details:
                    logger.debug(f"Детали: {e.details}")
                
                if error_count >= max_errors:
                    logger.critical("Слишком много ошибок подряд, завершение игры")
                    running = False
            
            except Exception as e:
                error_count += 1
                logger.error(f"Неожиданная ошибка: {type(e).__name__}: {e}")
                logger.debug(traceback.format_exc())
                
                if error_count >= max_errors:
                    logger.critical("Слишком много ошибок подряд, завершение игры")
                    running = False
        
        logger.info("Главный цикл игры завершен")
        
    except InitializationError as e:
        logger.critical(f"Ошибка инициализации: {e.message}")
        if e.details:
            logger.critical(f"Детали: {e.details}")
        print("\n" + "=" * 60)
        print("ОШИБКА ИНИЦИАЛИЗАЦИИ")
        print("=" * 60)
        print(e.message)
        if e.details:
            print(f"\nТехнические детали: {e.details}")
        print("\nПроверьте установку зависимостей:")
        print("  pip install -r requirements.txt")
        print("=" * 60)
        sys.exit(1)
    
    except KeyboardInterrupt:
        logger.info("Игра прервана пользователем (Ctrl+C)")
        print("\nИгра остановлена пользователем")
    
    except Exception as e:
        logger.critical(f"Критическая ошибка: {type(e).__name__}: {e}")
        logger.critical(traceback.format_exc())
        print("\n" + "=" * 60)
        print("КРИТИЧЕСКАЯ ОШИБКА")
        print("=" * 60)
        print(f"Произошла неожиданная ошибка: {type(e).__name__}")
        print(f"Сообщение: {e}")
        print("\nПодробности в логах (папка logs/)")
        print("=" * 60)
        traceback.print_exc()
        sys.exit(1)
    
    finally:
        logger.info("Завершение работы игры...")
        try:
            # Проверяем, что pygame был импортирован
            if pygame_module is not None:
                pygame_module.quit()
                logger.info("pygame завершен")
        except Exception as e:
            logger.error(f"Ошибка при завершении pygame: {e}")
        
        logger.info("=" * 60)
        logger.info("Игра завершена")
        logger.info("=" * 60)
        sys.exit(0)


if __name__ == "__main__":
    main()

