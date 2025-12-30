@echo off
chcp 65001 >nul
echo Проверка установки pygame-ce...
python -c "import pygame" 2>nul
if errorlevel 1 (
    echo pygame-ce не установлен. Устанавливаю...
    pip install pygame-ce
    if errorlevel 1 (
        echo Ошибка установки. Попробуйте вручную: pip install pygame-ce
        pause
        exit /b 1
    )
)

echo Запуск игры...
python main.py
if errorlevel 1 (
    echo.
    echo Произошла ошибка при запуске игры.
    pause
)



