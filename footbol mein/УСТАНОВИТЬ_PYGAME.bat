@echo off
chcp 65001 >nul
title Установка pygame-ce
color 0B

echo ========================================
echo    УСТАНОВКА PYGAME-CE
echo ========================================
echo.

echo [1/2] Проверка Python...
python --version
if errorlevel 1 (
    echo [ОШИБКА] Python не найден!
    echo Установите Python 3.12 с https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python установлен
echo.

echo [2/2] Установка pygame-ce...
echo Это может занять несколько минут...
echo.
pip install pygame-ce

if errorlevel 1 (
    echo.
    echo [ОШИБКА] Не удалось установить pygame-ce
    echo.
    echo Попробуйте вручную:
    echo   pip install pygame-ce
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo [УСПЕХ] pygame-ce установлен!
echo ========================================
echo.
echo Теперь можно запускать игру:
echo   - Двойной клик на ЗАПУСТИТЬ_ИГРУ.bat
echo   - Или python main.py
echo.
pause



