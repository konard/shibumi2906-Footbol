"""
Тестовый запуск игры с выводом в файл.
"""
import sys
import os

# Перенаправляем вывод в файл
log_file = open("launch_test.txt", "w", encoding="utf-8")
sys.stdout = log_file
sys.stderr = log_file

print("=" * 60)
print("Тестовый запуск игры")
print("=" * 60)
print()

try:
    print("1. Импорт settings...")
    import settings
    print("   OK")
    print()
    
    print("2. Импорт utils...")
    from src.utils.logger import setup_logger
    from src.utils.errors import InitializationError
    print("   OK")
    print()
    
    print("3. Проверка pygame...")
    try:
        import pygame
        print(f"   OK - версия: {pygame.version.ver}")
    except ImportError as e:
        print(f"   ОШИБКА: {e}")
        print("   pygame-ce не установлен!")
        log_file.close()
        sys.exit(1)
    print()
    
    print("4. Импорт manager...")
    from src.manager import GameStateManager, GameState
    print("   OK")
    print()
    
    print("5. Запуск main...")
    from main import main
    print("   Запускаю игру...")
    print()
    
    main()
    
except Exception as e:
    print(f"\nОШИБКА: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    log_file.close()
    sys.exit(1)

log_file.close()



