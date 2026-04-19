import os
from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_FILE = Path('test.db')
if DB_FILE.exists():
    DB_FILE.unlink()
os.environ['DATABASE_URL'] = 'sqlite:///./test.db'

from app.database import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402

engine = create_engine('sqlite:///./test.db', connect_args={'check_same_thread': False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_full_crud_flow():
    user = client.post('/api/users', json={'name': 'Alex', 'email': 'alex@example.com'})
    assert user.status_code == 200
    user_id = user.json()['id']

    updated_user = client.put(f'/api/users/{user_id}', json={'name': 'Alex K', 'email': 'alex.k@example.com'})
    assert updated_user.status_code == 200
    assert updated_user.json()['name'] == 'Alex K'

    project = client.post('/api/projects', json={'title': 'Core', 'description': 'Main app', 'owner_id': user_id})
    assert project.status_code == 200
    project_id = project.json()['id']

    task = client.post('/api/tasks', json={'title': 'Setup CI', 'status': 'todo', 'project_id': project_id})
    assert task.status_code == 200
    task_id = task.json()['id']

    task_update = client.put(
        f'/api/tasks/{task_id}',
        json={'title': 'Setup CI/CD', 'status': 'done', 'project_id': project_id},
    )
    assert task_update.status_code == 200
    assert task_update.json()['status'] == 'done'

    users = client.get('/api/users')
    projects = client.get('/api/projects')
    tasks = client.get('/api/tasks')
    assert users.status_code == projects.status_code == tasks.status_code == 200
    assert len(users.json()) == len(projects.json()) == len(tasks.json()) == 1

    assert client.delete(f'/api/tasks/{task_id}').status_code == 204
    assert client.delete(f'/api/projects/{project_id}').status_code == 204
    assert client.delete(f'/api/users/{user_id}').status_code == 204


def test_validation_and_not_found_responses():
    short_name = client.post('/api/users', json={'name': 'A', 'email': 'a@example.com'})
    assert short_name.status_code == 422

    missing_project = client.post('/api/tasks', json={'title': 'Task', 'status': 'todo', 'project_id': 9999})
    assert missing_project.status_code == 404
    assert missing_project.json()['detail'] == 'Project not found'


def test_unique_email_returns_conflict():
    first = client.post('/api/users', json={'name': 'John Doe', 'email': 'john@example.com'})
    assert first.status_code == 200

    duplicate = client.post('/api/users', json={'name': 'Johnny', 'email': 'john@example.com'})
    assert duplicate.status_code == 409
    assert duplicate.json()['detail'] == 'User with this email already exists'
