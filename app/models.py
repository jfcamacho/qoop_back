# app/models.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime, timedelta

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    subscribed = Column(Boolean, default=False)
    hashed_password = Column(String)  # Contraseña encriptada
    projects = relationship("Project", back_populates="owner")
    tasks = relationship("Task", back_populates="user")  # Relación con tareas
    subscription = relationship("Subscription", back_populates="user", uselist=False)  # Relación Uno a Uno
    
class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    tasks = relationship("Task", back_populates="project")
    owner = relationship("User", back_populates="projects")
    
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    completed = Column(Integer, default=0)  # 0 = pendiente, 1 = completada
    project_id = Column(Integer, ForeignKey("projects.id"))
    user_id = Column(Integer, ForeignKey("users.id"))  # Relación con el usuario
    project = relationship("Project", back_populates="tasks")
    user = relationship("User", back_populates="tasks")  # Relación con el usuario

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    start_date = Column(DateTime, default=datetime.utcnow)  # Fecha de inicio por defecto: ahora
    end_date = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=30))  # Por defecto, 30 días después
    paid = Column(Boolean, default=False)  # Estado de pago
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)  # Relación Uno a Uno con User
    user = relationship("User", back_populates="subscription")
