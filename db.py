from sqlalchemy import create_engine, Column, Integer, String, Time, Date, Boolean,ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from dotenv import load_dotenv
import os

env_path = r"D:\chat_bot_schadular\.env"
load_dotenv(dotenv_path=env_path)


engine_path = os.getenv(key="POSTGRESS_DB")
engine = create_engine(url=engine_path, echo=True)

Base = declarative_base()

class WeekDays(Base):
    __tablename__ = "week_days"
    id = Column(Integer, primary_key=True, autoincrement=True)
    working_date = Column(Date, default=func.current_date(), nullable=False) 
    day_id = Column(Integer, nullable=False)
    days = Column(String(25))



class WorkingHours(Base):
    __tablename__ = "working_hours"
    id = Column(Integer, primary_key=True, autoincrement=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    break_start = Column(Time, nullable=False)
    break_end = Column(Time, nullable=False)
    status = Column(Boolean, default=True, nullable=False)


class Weekly_hours(Base):
    __tablename__ = "Weekly_hours"
    id = Column(Integer, primary_key=True, autoincrement=True)
    week_days_id = Column(Integer, ForeignKey("week_days.id"), nullable=False)
    working_hours_id = Column(Integer, ForeignKey("working_hours.id"), nullable=False)
