from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from . import models, schemas


def _get_or_404(db: Session, model, item_id: int, entity_name: str):
    instance = db.query(model).filter(model.id == item_id).first()
    if not instance:
        raise HTTPException(status_code=404, detail=f"{entity_name} not found")
    return instance


def _commit_or_409(db: Session, duplicate_field: str = "Resource"):
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"{duplicate_field} already exists")


# Users

def create_user(db: Session, payload: schemas.UserCreate):
    user = models.User(**payload.model_dump())
    db.add(user)
    _commit_or_409(db, "User with this email")
    db.refresh(user)
    return user


def list_users(db: Session):
    return db.query(models.User).order_by(models.User.id).all()


def get_user(db: Session, user_id: int):
    return _get_or_404(db, models.User, user_id, "User")


def update_user(db: Session, user_id: int, payload: schemas.UserUpdate):
    user = get_user(db, user_id)
    for k, v in payload.model_dump().items():
        setattr(user, k, v)
    _commit_or_409(db, "User with this email")
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    db.delete(user)
    db.commit()


# Projects

def create_project(db: Session, payload: schemas.ProjectCreate):
    _ = get_user(db, payload.owner_id)
    project = models.Project(**payload.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def list_projects(db: Session):
    return db.query(models.Project).order_by(models.Project.id).all()


def get_project(db: Session, project_id: int):
    return _get_or_404(db, models.Project, project_id, "Project")


def update_project(db: Session, project_id: int, payload: schemas.ProjectUpdate):
    _ = get_user(db, payload.owner_id)
    project = get_project(db, project_id)
    for k, v in payload.model_dump().items():
        setattr(project, k, v)
    db.commit()
    db.refresh(project)
    return project


def delete_project(db: Session, project_id: int):
    project = get_project(db, project_id)
    db.delete(project)
    db.commit()


# Tasks

def create_task(db: Session, payload: schemas.TaskCreate):
    _ = get_project(db, payload.project_id)
    task = models.Task(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def list_tasks(db: Session):
    return db.query(models.Task).order_by(models.Task.id).all()


def get_task(db: Session, task_id: int):
    return _get_or_404(db, models.Task, task_id, "Task")


def update_task(db: Session, task_id: int, payload: schemas.TaskUpdate):
    _ = get_project(db, payload.project_id)
    task = get_task(db, task_id)
    for k, v in payload.model_dump().items():
        setattr(task, k, v)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int):
    task = get_task(db, task_id)
    db.delete(task)
    db.commit()
