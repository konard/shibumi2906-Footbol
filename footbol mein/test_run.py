"""
Тестовый скрипт для проверки запуска игры.
"""
import sys

print("=" * 60)
print("Проверка запуска игры")
print("=" * 60)
print()

# Проверка Python
print("1. Проверка Python...")
print(f"   Версия: {sys.version}")
print("   ✓ OK")
print()

# Проверка импорта settings
print("2. Проверка импорта settings...")
try:
    import settings
    print("   ✓ settings импортирован успешно")
except Exception as e:
    print(f"   ✗ Ошибка: {e}")
    sys.exit(1)
print()

# Проверка импорта utils
print("3. Проверка импорта utils...")
try:
    from src.utils.logger import setup_logger
    from src.utils.errors import InitializationError
    print("   ✓ utils импортированы успешно")
except Exception as e:
    print(f"   ✗ Ошибка: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
print()

# Проверка pygame
print("4. Проверка pygame...")
try:
    import pygame
    print(f"   ✓ pygame установлен (версия: {pygame.version.ver})")
except ImportError as e:
    print(f"   ✗ pygame не установлен: {e}")
    print("   Установите: pip install pygame-ce")
    sys.exit(1)
print()

# Проверка импорта основных модулей
print("5. Проверка импорта игровых модулей...")
try:
    from src.manager import GameStateManager, GameState
    print("   ✓ GameStateManager импортирован")
except Exception as e:
    print(f"   ✗ Ошибка импорта GameStateManager: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
print()

print("=" * 60)
print("Все проверки пройдены! Запуск игры...")
print("=" * 60)
print()

# Запуск игры
try:
    from main import main
    main()
except Exception as e:
    print(f"\n✗ Ошибка при запуске игры: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)



