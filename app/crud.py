from . import models, schemas, database
from sqlalchemy.orm import Session
from datetime import date, timedelta

def create_child(db: Session, child: schemas.ChildCreate):
    db_child = models.Child(**child.dict())
    db.add(db_child)
    db.commit()
    db.refresh(db_child)
    return db_child

def create_vaccine(db: Session, vac: schemas.VaccineCreate):
    db_vac = models.Vaccine(**vac.dict())
    db.add(db_vac)
    db.commit()
    db.refresh(db_vac)
    return db_vac

def create_schedule(db: Session, schedule: schemas.ScheduleCreate):
    db_schedule = models.Schedule(**schedule.dict())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

def get_pending_schedules(db: Session):
    return db.query(models.Schedule).filter(models.Schedule.done == False).all()
