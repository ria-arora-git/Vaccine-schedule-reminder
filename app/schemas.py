from pydantic import BaseModel
from datetime import date


class ChildBase(BaseModel):
    name: str
    parent_email: str
    birth_date: date


class ChildCreate(ChildBase):
    pass


class Child(ChildBase):
    id: int

    class Config:
        from_attributes = True


class VaccineBase(BaseModel):
    name: str
    due_age_weeks: int


class VaccineCreate(VaccineBase):
    pass


class Vaccine(VaccineBase):
    id: int

    class Config:
        from_attributes = True


class ScheduleBase(BaseModel):
    child_id: int
    vaccine_name: str
    scheduled_date: date


class ScheduleCreate(ScheduleBase):
    pass


class Schedule(ScheduleBase):
    id: int
    done: bool

    class Config:
        from_attributes = True
