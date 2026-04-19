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
- Быстрый запуск **одной командой** через Docker Compose.

## Запуск одной командой (Docker Compose)
```bash
docker compose up --build
```

После старта откройте: http://127.0.0.1:8000

Сервис `app` автоматически подключится к `PostgreSQL` в контейнере `db`.

## Локальный запуск без Docker
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
