# Скрипт запуска игры с проверкой зависимостей
Write-Host "Проверка установки pygame-ce..." -ForegroundColor Yellow

try {
    python -c "import pygame" 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "pygame не установлен"
    }
    Write-Host "pygame-ce установлен" -ForegroundColor Green
} catch {
    Write-Host "pygame-ce не установлен. Устанавливаю..." -ForegroundColor Yellow
    pip install pygame-ce
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Ошибка установки. Попробуйте вручную: pip install pygame-ce" -ForegroundColor Red
        Read-Host "Нажмите Enter для выхода"
        exit 1
    }
}

Write-Host "Запуск игры..." -ForegroundColor Green
python main.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Произошла ошибка при запуске игры." -ForegroundColor Red
    Read-Host "Нажмите Enter для выхода"
}



