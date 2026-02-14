from fastapi import FastAPI, Depends, File, UploadFile
from sqlalchemy.orm import Session
from . import crud, models, schemas, database
import shutil
import os
from .ocr import extract_text
from .parser import parse_vaccine_text
from datetime import timedelta
from .scheduler import scheduler
from .database import get_db
from .schemas import ChildCreate

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)


@app.post("/upload-sheet/")
async def upload_sheet(
    child_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    raw_text = extract_text(file_path)
    vaccines = parse_vaccine_text(raw_text)

    child = db.query(models.Child).filter(
        models.Child.id == child_id
    ).first()

    if not child:
        return {"error": "Child not found"}

    created = []

    for vac in vaccines:
        vaccine_name = vac["vaccine_name"]
        weeks = vac["due_age_weeks"]

        due_date = child.birth_date + timedelta(weeks=weeks)

        new_schedule = models.Schedule(
            child_id=child_id,
            vaccine_name=vaccine_name,
            scheduled_date=due_date,
            done=False
        )


        db.add(new_schedule)

        created.append({
            "vaccine_name": vaccine_name,
            "due_date": str(due_date)
        })

    db.commit()

    return {
        "parsed_vaccines": vaccines,
        "created_schedules": created
    }


@app.post("/child/")
def create_child(
    child: ChildCreate,
    db: Session = Depends(get_db)
):
    new_child = models.Child(
        name=child.name,
        birth_date=child.birth_date,
        parent_email=child.parent_email
    )

    db.add(new_child)
    db.commit()
    db.refresh(new_child)

    return new_child


@app.post("/vaccine/")
def create_vaccine(
    vac: schemas.VaccineCreate,
    db: Session = Depends(get_db)
):
    return crud.create_vaccine(db, vac)


@app.post("/schedule/")
def create_schedule(schedule: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    new_schedule = models.Schedule(
        child_id=schedule.child_id,
        vaccine_name=schedule.vaccine_name,
        scheduled_date=schedule.scheduled_date,
        done=False
    )

    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)

    return new_schedule



@app.get("/children/")
def get_children(db: Session = Depends(get_db)):
    children = db.query(models.Child).all()

    return [
        {
            "id": c.id,
            "name": c.name,
            "parent_email": c.parent_email
        }
        for c in children
    ]


@app.get("/pending/")
def get_pending(db: Session = Depends(get_db)):
    schedules = db.query(models.Schedule).filter(
        models.Schedule.done == False
    ).all()

    return [
        {
            "id": s.id,
            "child_name": s.child.name,
            "vaccine_name": s.vaccine_name,
            "scheduled_date": str(s.scheduled_date)
        }
        for s in schedules
    ]



@app.put("/mark-done/{schedule_id}")
def mark_done(schedule_id: int, db: Session = Depends(get_db)):
    schedule = db.query(models.Schedule).filter(
        models.Schedule.id == schedule_id
    ).first()

    if not schedule:
        return {"error": "Schedule not found"}

    schedule.done = True
    db.commit()

    return {"message": "Marked as done"}


@app.on_event("startup")
def start_scheduler():
    scheduler.start()
