# app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas, auth
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(name=user.name, username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: schemas.UserCreate):
    if len(user.password) > 3:
        hashed_password = auth.get_password_hash(user.password)
    db_user = get_user(db, user_id)
    if db_user:
        db_user.name = user.name
        db_user.username = user.username
        db_user.email = user.email
        if len(user.password) > 3:
            db_user.hashed_password = hashed_password
        db.commit()
        db.refresh(db_user)
    return db_user

def update_user_subscription(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db_user.subscribed = True
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

def create_project(db: Session, project: schemas.ProjectCreate, user_id: int):
    db_project = models.Project(title=project.title, description=project.description, owner_id=user_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def update_project(db: Session, project_id: int, project: schemas.Project):
    db_project = get_project(db, project_id)
    if db_project:
        db_project.title = project.title
        db_project.description = project.description
        db.commit()
        db.refresh(db_project)
    return db_project

def create_task(db: Session, task: schemas.TaskCreate, project_id: int):
    db_task = models.Task(title=task.title, description=task.description, project_id=project_id, user_id=task.user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_projects_by_user(db: Session, user_id: int):
    return db.query(models.Project).filter(models.Project.owner_id == user_id).all()

def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()

def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Project).offset(skip).limit(limit).all()

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).options(joinedload(models.Task.user)).offset(skip).limit(limit).all()

def get_tasks_by_project(db: Session, project_id: int):
    return db.query(models.Task).options(joinedload(models.Task.user)).filter(models.Task.project_id == project_id).all()

def update_task_status(db: Session, task_id: int, task: schemas.Task):
    taskU = db.query(models.Task).filter(models.Task.id == task_id).first()
    if taskU:
        taskU.title = task.title
        taskU.user_id = task.user_id
        taskU.description = task.description
        taskU.completed = task.completed
        db.commit()
        db.refresh(taskU)
    return taskU

def delete_task(db: Session, task_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        return {"error": "Task not found"}
    db.delete(task)
    db.commit()
    return True

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        return None
    if not auth.verify_password(password, user.hashed_password):
        return None
    return user

def create_subscription(db: Session, user_id: int, subscription: schemas.SubscriptionCreate):
    db_subscription = models.Subscription(
        user_id=user_id,
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow() + timedelta(days=30),
        paid=subscription.paid
    )
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

def get_subscription_by_user(db: Session, user_id: int):
    return db.query(models.Subscription).filter(models.Subscription.user_id == user_id).first()

def update_subscription(db: Session, user_id: int, subscription: schemas.SubscriptionBase):
    db_subscription = db.query(models.Subscription).filter(models.Subscription.user_id == user_id).first()
    if db_subscription:
        db_subscription.start_date = subscription.start_date
        db_subscription.end_date = subscription.end_date
        db_subscription.paid = subscription.paid
        db.commit()
        db.refresh(db_subscription)
    return db_subscription

def delete_subscription(db: Session, user_id: int):
    db_subscription = db.query(models.Subscription).filter(models.Subscription.user_id == user_id).first()
    if db_subscription:
        db.delete(db_subscription)
        db.commit()
    return db_subscription

def delete_expired_subscriptions(db: Session):
    expired_subscriptions = db.query(models.Subscription).filter(
        models.Subscription.end_date < datetime.now()
    ).all()
    
    for subscription in expired_subscriptions:
        db.delete(subscription)
    
    db.commit()