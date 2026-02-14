from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy import Date

class Child(Base):
    __tablename__ = "children"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    parent_email = Column(String)
    birth_date = Column(Date)

    schedules = relationship("Schedule", back_populates="child")


class Vaccine(Base):
    __tablename__ = "vaccines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    due_age_weeks = Column(Integer)


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("children.id"))
    vaccine_id = Column(Integer, ForeignKey("vaccines.id"))
    scheduled_date = Column(Date)
    done = Column(Boolean, default=False)

    child = relationship("Child", back_populates="schedules")
