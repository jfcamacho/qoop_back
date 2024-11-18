# app/routers/tasks.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..dependencies import get_db, get_current_user
from typing import List
from ..email import send_email

router = APIRouter()

@router.post("/tasks/{project_id}", response_model=schemas.Task)
def create_task(project_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=task.user_id)
    if db_user:
        db_task = crud.create_task(db=db, task=task, project_id=project_id)
        if db_task:
            send_email("Assigned Task", "You have been assigned a new task", db_user.email)
    return db_task

@router.get("/tasks", response_model=List[schemas.Task])
def read_tasks(
    db: Session = Depends(get_db),
    current_user: schemas.Task=Depends(get_current_user),
    skip: int = 0, limit: int = 100):
    return crud.get_tasks(db=db, skip=skip, limit=limit)

@router.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.get("/tasks/project/{project_id}", response_model=List[schemas.Task])
def read_task(project_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_tasks_by_project(db, project_id=project_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.Task, db: Session = Depends(get_db)):
    print(task)
    db_task = crud.update_task_status(db, task_id=task_id, task=task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.delete_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task
