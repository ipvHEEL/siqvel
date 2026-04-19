# Siqvel Platform

Полноценный CRUD-проект с бэкендом на FastAPI и фронтендом на чистом HTML/CSS/JS.

## Что есть
- CRUD для сущностей: `users`, `projects`, `tasks`.
- Поддержка популярных SQL-баз через `SQLAlchemy`:
  - SQLite
  - PostgreSQL
  - MySQL
- Красивый одностраничный интерфейс (glassmorphism + gradients).
- Автотесты (pytest) для API.

## Запуск
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Откройте: http://127.0.0.1:8000

## Конфигурация БД
Используйте переменную окружения:

```bash
export DATABASE_URL="sqlite:///./app.db"
# или
export DATABASE_URL="postgresql+psycopg://user:pass@localhost:5432/siqvel"
# или
export DATABASE_URL="mysql+pymysql://user:pass@localhost:3306/siqvel"
```

По умолчанию используется SQLite (`sqlite:///./app.db`).

## Тесты
```bash
pytest -q
```
