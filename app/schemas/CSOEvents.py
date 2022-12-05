from datetime import date, time
from pydantic import BaseModel
from typing import Optional


class CSOEventSchema(BaseModel):
    event_name: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    description: Optional[str] = None
    category: Optional[str] = None
    gender: Optional[str] = None
    supervisor: Optional[str] = None
    hours_credit: Optional[int] = None

    class Config:
        orm_mode = True


class CreateCSOEvent(CSOEventSchema):
    event_name: str
    location: str
    start_date: date
    end_date: date
    start_time: time
    end_time: time
    description: str
    category: str
    gender: str
    supervisor: str
    hours_credit: int

    class Config:
        orm_mode = True


class CSOEventUpdate(BaseModel):
    pass
