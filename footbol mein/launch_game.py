"""
Скрипт для запуска игры с автоматической проверкой зависимостей.
"""
import sys
import subprocess

def check_and_install_pygame():
    """Проверка и установка pygame-ce."""
    try:
        import pygame
        print(f"✓ pygame-ce установлен (версия: {pygame.version.ver})")
        return True
    except ImportError:
        print("✗ pygame-ce не установлен")
        print("Устанавливаю pygame-ce...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame-ce", "--quiet"])
            print("✓ pygame-ce успешно установлен")
            return True
        except subprocess.CalledProcessError:
            print("✗ Ошибка установки pygame-ce")
            print("\nПопробуйте установить вручную:")
            print("  pip install pygame-ce")
            return False

if __name__ == "__main__":
    print("=" * 60)
    print("Football Game - Запуск")
    print("=" * 60)
    print()
    
    if check_and_install_pygame():
        print()
        print("Запуск игры...")
        print("=" * 60)
        print()
        # Импортируем и запускаем main
        from main import main
        main()
    else:
        print("\nНе удалось запустить игру. Установите зависимости:")
        print("  pip install -r requirements.txt")
        input("\nНажмите Enter для выхода...")
        sys.exit(1)



