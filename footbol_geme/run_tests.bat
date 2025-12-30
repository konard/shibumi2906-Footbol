@echo off
chcp 65001 >nul
echo ========================================
echo    ЗАПУСК ТЕСТОВ
echo ========================================
echo.

echo Проверка установки pytest...
python -c "import pytest" >nul 2>&1
if errorlevel 1 (
    echo pytest не установлен. Устанавливаю...
    pip install pytest pytest-cov
    if errorlevel 1 (
        echo Ошибка установки pytest
        pause
        exit /b 1
    )
)

echo.
echo Запуск тестов...
echo.

pytest -v --cov=src --cov-report=term-missing

if errorlevel 1 (
    echo.
    echo ========================================
    echo Некоторые тесты не прошли
    echo ========================================
) else (
    echo.
    echo ========================================
    echo Все тесты прошли успешно!
    echo ========================================
)

echo.
pause



