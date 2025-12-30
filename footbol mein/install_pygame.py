"""
Скрипт для установки pygame-ce.
"""
import sys
import subprocess

print("=" * 60)
print("Установка pygame-ce")
print("=" * 60)
print()

# Проверка Python
print("Проверка Python...")
print(f"Версия: {sys.version}")
print("OK")
print()

# Установка pygame-ce
print("Установка pygame-ce...")
print("Это может занять несколько минут...")
print()

try:
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", "pygame-ce", "--upgrade"
    ])
    print()
    print("=" * 60)
    print("УСПЕХ! pygame-ce установлен!")
    print("=" * 60)
    print()
    print("Теперь можно запускать игру:")
    print("  python main.py")
    print("  или двойной клик на ЗАПУСТИТЬ_ИГРУ.bat")
    print()
    
except subprocess.CalledProcessError as e:
    print()
    print("=" * 60)
    print("ОШИБКА установки!")
    print("=" * 60)
    print()
    print("Попробуйте вручную:")
    print("  pip install pygame-ce")
    print()
    input("Нажмите Enter для выхода...")
    sys.exit(1)
except KeyboardInterrupt:
    print()
    print("Установка прервана пользователем")
    sys.exit(1)



