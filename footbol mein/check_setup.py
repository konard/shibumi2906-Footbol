"""
Скрипт для проверки готовности к запуску игры.
"""
import sys

def check_python_version():
    """Проверка версии Python."""
    version = sys.version_info
    print(f"Python версия: {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 12):
        print("⚠️  Внимание: Рекомендуется Python 3.12 или выше")
        return False
    print("✅ Версия Python подходит")
    return True

def check_pygame():
    """Проверка установки pygame-ce."""
    try:
        import pygame
        print(f"✅ pygame-ce установлен (версия: {pygame.version.ver})")
        return True
    except ImportError:
        print("❌ pygame-ce не установлен")
        print("\nДля установки выполните:")
        print("  pip install -r requirements.txt")
        return False

def check_files():
    """Проверка наличия необходимых файлов."""
    import os
    required_files = [
        "main.py",
        "settings.py",
        "src/manager.py",
        "src/entities/player.py",
        "src/entities/ball.py",
        "src/ai/bot.py"
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print(f"❌ Отсутствуют файлы: {', '.join(missing)}")
        return False
    else:
        print("✅ Все необходимые файлы на месте")
        return True

if __name__ == "__main__":
    print("=" * 50)
    print("Проверка готовности к запуску игры")
    print("=" * 50)
    print()
    
    python_ok = check_python_version()
    print()
    
    pygame_ok = check_pygame()
    print()
    
    files_ok = check_files()
    print()
    
    print("=" * 50)
    if python_ok and pygame_ok and files_ok:
        print("✅ ВСЁ ГОТОВО! Можно запускать игру:")
        print("   python main.py")
    else:
        print("❌ Требуется установка зависимостей")
        print("   Выполните: pip install -r requirements.txt")
        print("   Или запустите: setup.bat")
    print("=" * 50)



