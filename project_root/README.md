# FastAPI Tasks API

REST API для управления задачами: создание, просмотр, обновление, удаление, сортировка, топ5 задач по приоритету.

---

## Технологии

- Python 3.12
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Pytest
- Coverage

---

## Установка зависимостей

Создайте виртуальное окружение и установите зависимости:

```bash
python -m venv venv

source ven/bin/activate

pip install -r requirements.txt

# Запустите FastAPI-приложение:
uvicorn src.main:app --reload

# Перейдите в корень проекта и выполните:
pytest

# Проверка покрытия:
coverage run -m pytest
coverage report -m

# HTML-отчет:
coverage html
```


