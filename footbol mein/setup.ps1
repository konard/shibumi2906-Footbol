# Скрипт установки для PowerShell
Write-Host "Создание виртуального окружения..." -ForegroundColor Green
python -m venv venv

Write-Host "Активация виртуального окружения..." -ForegroundColor Green
& .\venv\Scripts\Activate.ps1

Write-Host "Обновление pip..." -ForegroundColor Green
python -m pip install --upgrade pip

Write-Host "Установка зависимостей..." -ForegroundColor Green
pip install -r requirements.txt

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Установка завершена!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Для активации виртуального окружения в будущем используйте:" -ForegroundColor Yellow
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""
Write-Host "Для запуска игры:" -ForegroundColor Yellow
Write-Host "  python main.py" -ForegroundColor White
Write-Host ""



