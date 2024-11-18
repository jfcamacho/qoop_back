# app/main.py
from fastapi import FastAPI
from .database import engine
from .models import Base
from .routers import users, projects, tasks, subscription
from fastapi.middleware.cors import CORSMiddleware
from .scheduler import start_scheduler

app = FastAPI()

start_scheduler()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Cambia esto según tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear las tablas
Base.metadata.create_all(bind=engine)

# Incluir routers
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(subscription.router)
