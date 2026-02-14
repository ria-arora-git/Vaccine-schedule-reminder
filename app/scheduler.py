from apscheduler.schedulers.background import BackgroundScheduler
from datetime import date
from .database import SessionLocal
from . import models
from .email import send_reminder

scheduler = BackgroundScheduler()

def check_reminders():
    print("Running weekly reminder check...")

    db = SessionLocal()
    today = date.today()

    schedules = db.query(models.Schedule).filter(models.Schedule.done == False).all()

    for s in schedules:
        if True:
            print(f"Sending reminder for {s.id}")
            send_reminder(
                s.child.parent_email,
                "Upcoming Vaccine",
                s.scheduled_date
            )

    db.close()

scheduler.add_job(check_reminders, "interval", minutes=1)
