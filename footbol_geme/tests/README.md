# Тесты для Football Game

## Запуск тестов

### Все тесты
```bash
pytest
```

### С покрытием кода
```bash
pytest --cov=src --cov-report=html
```

После выполнения откройте `htmlcov/index.html` в браузере для просмотра отчета о покрытии.

### Конкретный файл тестов
```bash
pytest tests/test_entities.py
```

### Конкретный тест
```bash
pytest tests/test_entities.py::TestEntity::test_entity_creation
```

### Вербозный вывод
```bash
pytest -v
```

## Структура тестов

- `test_entities.py` - Тесты для игровых сущностей (Entity, Ball, Player)
- `test_physics.py` - Тесты для физики столкновений
- `test_ai.py` - Тесты для ИИ
- `test_errors.py` - Тесты для обработки ошибок

## Покрытие кода

Цель: покрытие не менее 80% кода.

Текущее покрытие можно проверить:
```bash
pytest --cov=src --cov-report=term-missing
```

## Добавление новых тестов

При добавлении новых функций обязательно добавляйте тесты:

1. Создайте тестовый файл `test_<module_name>.py`
2. Импортируйте тестируемый модуль
3. Создайте класс `Test<ClassName>`
4. Добавьте методы `test_<function_name>`

Пример:
```python
def test_my_function():
    """Тест для функции my_function."""
    result = my_function(input)
    assert result == expected_output
```



