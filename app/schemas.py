from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None

class TaskCreate(TaskBase):
    user_id: int  # Agregar user_id para asociar la tarea con un usuario

class UserInTask(BaseModel):
    name: str  # Solo el nombre del usuario

    class Config:
        orm_mode = True
        
class ProjectInTask(BaseModel):
    title: str  # Solo el nombre del usuario

    class Config:
        orm_mode = True

class Task(TaskBase):
    id: int
    completed: int
    project_id: int
    user_id: int  # Incluir user_id para indicar el usuario que posee la tarea
    user: UserInTask  # Relación con el usuario, usando un modelo para el nombre del usuario
    project: ProjectInTask

    class Config:
        orm_mode = True

class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    owner_id: int
    tasks: List[Task] = []  # Incluir tareas asociadas al proyecto

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: str
    name: str
    subscribed: bool

class UserCreate(UserBase):
    password: str

class userSubscribed(UserBase):
    subscribed: bool

class User(UserBase):
    id: int
    projects: List[Project] = []  # Relación con los proyectos del usuario
    tasks: List[Task] = []  # Relación con las tareas del usuario

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User  # Incluir el usuario en el token

class TokenData(BaseModel):
    username: str | None = None

class SubscriptionBase(BaseModel):
    start_date: datetime
    end_date: datetime
    paid: bool

class SubscriptionCreate(BaseModel):
    paid: bool = False  # Campo opcional al crear una suscripción

class Subscription(SubscriptionBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True