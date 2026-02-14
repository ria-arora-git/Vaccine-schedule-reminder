from pydantic import BaseModel
from datetime import date
from typing import Optional

class ChildBase(BaseModel):
    name: str
    parent_email: str
    birth_date: date


class ChildCreate(ChildBase):
    pass

class VaccineBase(BaseModel):
    name: str
    due_age_weeks: int

class VaccineCreate(VaccineBase):
    pass

class ScheduleBase(BaseModel):
    child_id: int
    vaccine_id: int
    scheduled_date: date

class ScheduleCreate(ScheduleBase):
    pass

class Schedule(ScheduleBase):
    id: int
    done: bool

    class Config:
        orm_mode = True
