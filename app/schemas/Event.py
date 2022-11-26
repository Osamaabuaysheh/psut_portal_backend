from datetime import date, time
from pydantic import BaseModel
from typing import Optional
from app.schemas.organizer import OrganizerSchema


class EventSchema(BaseModel):
    # event_id: Optional[int] = None
    event_name: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    description: Optional[str] = None
    organizers: Optional[list[str]] = None

    class Config:
        orm_mode = True


class CreateEvent(EventSchema):
    event_name: str
    location: str
    start_date: date
    end_date: date
    start_time: time
    end_time: time
    organizers: list[str]
    description: str
    owner_id: int

    class Config:
        orm_mode = True


class EventOut(EventSchema):
    event_id: Optional[int] = None
    event_name: str
    location: str
    start_date: date
    end_date: date

    start_time: time
    end_time: time
    description: str
    organizers: list[OrganizerSchema]
    image: str

    class Config:
        orm_mode = True


class ClubsEventSchema(EventSchema):
    club_name: str

    class Config:
        orm_mode = True


class ClubEventOut(EventOut):
    club_name: str

    pass


class ClubEventCreate(EventSchema):
    pass
