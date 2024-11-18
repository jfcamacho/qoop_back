# app/routers/subscription.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..dependencies import get_db, get_current_user
from typing import List
from datetime import datetime
from app.database import SessionLocal
from ..email import send_email

router = APIRouter()

@router.post("/subscriptions/{user_id}", response_model=schemas.Subscription)
def create_subscription(user_id: int, subscription: schemas.SubscriptionCreate, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    existing_subscription = crud.get_subscription_by_user(db, user_id=user_id)
    if existing_subscription:
        raise HTTPException(status_code=400, detail=(str(existing_subscription.id)))
    db_subscription = crud.create_subscription(db=db, user_id=user_id, subscription=subscription)
    if db_subscription:
            send_email("Successful subscription", "Your subscription has been successful", user.email)
    return db_subscription

# Obtener la suscripción de un usuario
@router.get("/subscriptions/{user_id}", response_model=schemas.Subscription)
def read_subscription(user_id: int, db: Session = Depends(get_db)):
    subscription = crud.get_subscription_by_user(db, user_id=user_id)
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription

# Actualizar la suscripción de un usuario
@router.put("/subscriptions/{user_id}", response_model=schemas.Subscription)
def update_subscription(user_id: int, subscription: schemas.SubscriptionBase, db: Session = Depends(get_db)):
    updated_subscription = crud.update_subscription(db=db, user_id=user_id, subscription=subscription)
    if not updated_subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return updated_subscription

# Eliminar la suscripción de un usuario
@router.delete("/subscriptions/{user_id}", response_model=schemas.Subscription)
def delete_subscription(user_id: int, db: Session = Depends(get_db)):
    deleted_subscription = crud.delete_subscription(db=db, user_id=user_id)
    if not deleted_subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return deleted_subscription