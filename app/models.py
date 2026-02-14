from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Child(Base):
    __tablename__ = "children"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    parent_email = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)

    schedules = relationship("Schedule", back_populates="child")


class Vaccine(Base):
    __tablename__ = "vaccines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    due_age_weeks = Column(Integer, nullable=False)

    schedules = relationship("Schedule", back_populates="vaccine")


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("children.id"))
    vaccine_name = Column(String)
    scheduled_date = Column(Date)
    done = Column(Boolean, default=False)

    child = relationship("Child", back_populates="schedules")
    vaccine = relationship("Vaccine", back_populates="schedules")
