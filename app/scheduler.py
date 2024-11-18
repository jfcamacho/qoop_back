import schedule
import time
from threading import Thread
from datetime import datetime
from .crud import delete_expired_subscriptions
from app.database import SessionLocal

# Función para eliminar las suscripciones caducadas
def delete_expired_subscriptions_cron():
    db = SessionLocal()
    try:
        delete_expired_subscriptions(db)
    except Exception as e:
        print(f"Error al eliminar suscripciones caducadas: {e}")
    finally:
        db.close()

schedule.every(1).minutes.do(delete_expired_subscriptions_cron)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

def start_scheduler():
    scheduler_thread = Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
