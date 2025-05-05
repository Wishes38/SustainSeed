from apscheduler.schedulers.background import BackgroundScheduler
from app.database import SessionLocal
from app.crud import daily_task

scheduler = BackgroundScheduler()

def assign_tasks_job():
    db = SessionLocal()
    daily_task.assign_daily_tasks_to_all_users(db)
    db.close()

def clear_tasks_job():
    db = SessionLocal()
    daily_task.clear_all_daily_tasks(db)
    db.close()

scheduler.add_job(assign_tasks_job, "cron", hour=0, minute=1)
scheduler.add_job(clear_tasks_job, "cron", hour=23, minute=59)

def start():
    scheduler.start()
