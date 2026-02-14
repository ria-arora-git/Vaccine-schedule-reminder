from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Child(Base):
    __tablename__ = "children"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    parent_email = Column(String)
    birth_date = Column(Date)

    schedules = relationship("Schedule", back_populates="child")


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("children.id"))
    vaccine_name = Column(String)
    scheduled_date = Column(Date)
    done = Column(Boolean, default=False)

    child = relationship("Child", back_populates="schedules")
