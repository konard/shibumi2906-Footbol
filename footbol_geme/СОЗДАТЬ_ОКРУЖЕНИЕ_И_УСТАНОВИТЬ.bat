@echo off
chcp 65001 >nul
title Создание окружения и установка pygame-ce
color 0B

echo ========================================
echo  СОЗДАНИЕ ВИРТУАЛЬНОГО ОКРУЖЕНИЯ
echo  И УСТАНОВКА PYGAME-CE
echo ========================================
echo.

echo [1/3] Проверка Python...
python --version
if errorlevel 1 (
    echo [ОШИБКА] Python не найден!
    pause
    exit /b 1
)
echo [OK] Python установлен
echo.

echo [2/3] Создание виртуального окружения...
if exist venv (
    echo [INFO] Папка venv уже существует, пропускаю создание
) else (
    python -m venv venv
    if errorlevel 1 (
        echo [ОШИБКА] Не удалось создать виртуальное окружение
        pause
        exit /b 1
    )
    echo [OK] Виртуальное окружение создано
)
echo.

echo [3/3] Активация окружения и установка pygame-ce...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ОШИБКА] Не удалось активировать окружение
    pause
    exit /b 1
)

echo [INFO] Виртуальное окружение активировано
echo [INFO] Установка pygame-ce...
pip install --upgrade pip
pip install pygame-ce

if errorlevel 1 (
    echo [ОШИБКА] Не удалось установить pygame-ce
    pause
    exit /b 1
)

echo.
echo ========================================
echo [УСПЕХ] Всё готово!
echo ========================================
echo.
echo Виртуальное окружение создано и активировано
echo pygame-ce установлен в виртуальное окружение
echo.
echo Для запуска игры:
echo   1. Активируйте окружение: venv\Scripts\activate.bat
echo   2. Запустите: python main.py
echo.
echo Или используйте ЗАПУСТИТЬ_ИГРУ.bat
echo.
pause



