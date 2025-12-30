@echo off
chcp 65001 >nul
title Football Game - Запуск
color 0A

echo ========================================
echo    FOOTBALL GAME - ЗАПУСК
echo ========================================
echo.

echo [1/3] Проверка Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] Python не найден!
    echo Установите Python 3.12 с https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo [OK] Python установлен
echo.

echo [2/4] Проверка виртуального окружения...
if exist venv\Scripts\activate.bat (
    echo [OK] Виртуальное окружение найдено
    call venv\Scripts\activate.bat
    echo [OK] Окружение активировано
) else (
    echo [СОЗДАНИЕ] Создаю виртуальное окружение...
    python -m venv venv
    if errorlevel 1 (
        echo [ОШИБКА] Не удалось создать виртуальное окружение
        pause
        exit /b 1
    )
    call venv\Scripts\activate.bat
    echo [OK] Виртуальное окружение создано и активировано
)
echo.

echo [3/4] Проверка pygame-ce...
python -c "import pygame" >nul 2>&1
if errorlevel 1 (
    echo [УСТАНОВКА] pygame-ce не найден, устанавливаю...
    pip install --upgrade pip >nul 2>&1
    pip install pygame-ce --quiet
    if errorlevel 1 (
        echo [ОШИБКА] Не удалось установить pygame-ce
        echo Попробуйте вручную: pip install pygame-ce
        pause
        exit /b 1
    )
    echo [OK] pygame-ce установлен
) else (
    echo [OK] pygame-ce уже установлен
)
echo.

echo [4/4] Запуск игры...
echo.

echo.
echo ========================================
echo   ИГРА ЗАПУСКАЕТСЯ...
echo ========================================
echo.
echo Управление:
echo   WASD / Стрелки - движение
echo   SPACE - удар по мячу
echo   ENTER - начать игру
echo   ESC - выход
echo.
echo ========================================
echo.

python main.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo [ОШИБКА] Игра завершилась с ошибкой
    echo ========================================
    echo.
    pause
)

