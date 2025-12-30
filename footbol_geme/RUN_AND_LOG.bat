@echo off
cd /d "%~dp0"
echo Запуск игры...
echo.
python main.py > game_output.txt 2>&1
echo.
echo Результат сохранен в game_output.txt
echo.
type game_output.txt
echo.
pause



