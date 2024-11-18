# app/routers/projects.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from typing import List
from ..dependencies import get_db, get_current_user

router = APIRouter()

@router.post("/projects/{user_id}", response_model=schemas.Project)
def create_project(user_id: int, project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    # Aquí `user_id` es un parámetro de ruta
    return crud.create_project(db=db, user_id=user_id, project=project)

# @router.post("/projects/{user_id}", response_model=schemas.Project)
# def create_project(project: schemas.ProjectCreate, user_id: int, db: Session = Depends(get_db)):
#     return crud.create_project(db=db, project=project, user_id=user_id)

# @router.get("/users/me", response_model=List[schemas.User])
# def read_users(
#     db: Session = Depends(get_db),
#     current_user: schemas.User=Depends(get_current_user),
#     skip: int = 0, limit: int = 100):
#     return crud.get_users(db=db, skip=skip, limit=limit)

@router.get("/projects", response_model=List[schemas.Project])
def read_users(
    db: Session = Depends(get_db),
    current_user: schemas.Project=Depends(get_current_user),
    skip: int = 0, limit: int = 100):
    return crud.get_projects(db=db, skip=skip, limit=limit)

@router.get("/projects/{project_id}", response_model=schemas.Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    db_project = crud.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@router.put("/projects/{project_id}", response_model=schemas.Project)
def update_project(project_id: int, project: schemas.ProjectBase, db: Session = Depends(get_db)):
    db_project = crud.update_project(db, project_id=project_id, project=project)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@router.delete("/projects/{project_id}", response_model=schemas.Project)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    db_project = crud.delete_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project
