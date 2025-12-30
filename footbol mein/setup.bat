@echo off
chcp 65001 >nul
echo Создание виртуального окружения...
python -m venv venv

echo Активация виртуального окружения...
call venv\Scripts\activate.bat

echo Обновление pip...
python -m pip install --upgrade pip

echo Установка зависимостей...
pip install -r requirements.txt

echo.
echo ========================================
echo Установка завершена!
echo ========================================
echo.
echo Для активации виртуального окружения в будущем используйте:
echo   venv\Scripts\activate.bat
echo.
echo Для запуска игры:
echo   python main.py
echo.
pause



