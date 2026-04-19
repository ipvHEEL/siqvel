from pathlib import Path

from fastapi import Depends, FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Siqvel Platform API", version="1.0.0")

static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
def index():
    return FileResponse(static_dir / "index.html")


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/users", response_model=schemas.UserOut)
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, payload)


@app.get("/api/users", response_model=list[schemas.UserOut])
def list_users(db: Session = Depends(get_db)):
    return crud.list_users(db)


@app.get("/api/users/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(db, user_id)


@app.put("/api/users/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: int, payload: schemas.UserUpdate, db: Session = Depends(get_db)):
    return crud.update_user(db, user_id, payload)


@app.delete("/api/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    crud.delete_user(db, user_id)


@app.post("/api/projects", response_model=schemas.ProjectOut)
def create_project(payload: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(db, payload)


@app.get("/api/projects", response_model=list[schemas.ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    return crud.list_projects(db)


@app.get("/api/projects/{project_id}", response_model=schemas.ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db)):
    return crud.get_project(db, project_id)


@app.put("/api/projects/{project_id}", response_model=schemas.ProjectOut)
def update_project(project_id: int, payload: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    return crud.update_project(db, project_id, payload)


@app.delete("/api/projects/{project_id}", status_code=204)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    crud.delete_project(db, project_id)


@app.post("/api/tasks", response_model=schemas.TaskOut)
def create_task(payload: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, payload)


@app.get("/api/tasks", response_model=list[schemas.TaskOut])
def list_tasks(db: Session = Depends(get_db)):
    return crud.list_tasks(db)


@app.get("/api/tasks/{task_id}", response_model=schemas.TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    return crud.get_task(db, task_id)


@app.put("/api/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, payload: schemas.TaskUpdate, db: Session = Depends(get_db)):
    return crud.update_task(db, task_id, payload)


@app.delete("/api/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    crud.delete_task(db, task_id)
