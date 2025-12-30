# Инструкция по установке

## Шаг 1: Установка Python 3.12

Если у вас еще не установлен Python 3.12:

1. Скачайте Python 3.12.9 с официального сайта:
   - https://www.python.org/downloads/
   - Или прямая ссылка: https://www.python.org/ftp/python/3.12.9/python-3.12.9-amd64.exe

2. При установке **обязательно отметьте галочку "Add Python to PATH"**

3. Установите Python

## Шаг 2: Создание виртуального окружения и установка библиотек

### Вариант 1: Автоматическая установка (рекомендуется)

**Для Windows (Command Prompt или PowerShell):**

Запустите один из скриптов:
- `setup.bat` (для Command Prompt)
- `setup.ps1` (для PowerShell)

Если PowerShell блокирует выполнение скриптов, выполните:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Вариант 2: Ручная установка

1. Откройте терминал (Command Prompt или PowerShell) в папке проекта

2. Создайте виртуальное окружение:
```bash
python -m venv venv
```

3. Активируйте виртуальное окружение:

   **Для Command Prompt:**
   ```bash
   venv\Scripts\activate.bat
   ```

   **Для PowerShell:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

4. Обновите pip:
```bash
python -m pip install --upgrade pip
```

5. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Шаг 3: Запуск игры

После активации виртуального окружения:
```bash
python main.py
```

## Полезные команды

- **Деактивация виртуального окружения:**
  ```bash
  deactivate
  ```

- **Проверка установленных пакетов:**
  ```bash
  pip list
  ```

- **Проверка версии Python:**
  ```bash
  python --version
  ```

## Решение проблем

### Проблема: "python не является внутренней или внешней командой"
**Решение:** Python не добавлен в PATH. Переустановите Python с галочкой "Add Python to PATH"

### Проблема: PowerShell блокирует выполнение скриптов
**Решение:** Выполните:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Проблема: Ошибка при установке pygame-ce
**Решение:** Убедитесь, что у вас установлена последняя версия pip:
```bash
python -m pip install --upgrade pip
```



