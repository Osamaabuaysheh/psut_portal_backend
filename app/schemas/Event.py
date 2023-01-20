from datetime import date, time
from typing import Optional

from pydantic import BaseModel

from app.schemas.organizer import OrganizerSchema


class EventSchema(BaseModel):
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
    organizers: Optional[list[str]] = None
    description: str
    owner_id: int

    class Config:
        orm_mode = True


class UpadteEvent(BaseModel):
    event_name: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    description: Optional[str] = None
    image: Optional[str] = None

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
    owner_role: str

    class Config:
        orm_mode = True


class ClubsEventSchema(EventSchema):
    club_id: int

    class Config:
        orm_mode = True


class ClubEventOut(EventOut):
    club_name: str
    organizers: list[OrganizerSchema]


class ClubEventCreate(BaseModel):
    event_name: str
    location: str
    start_date: date
    end_date: date
    start_time: time
    end_time: time
    description: str
    club_organizer: int

    class Config:
        orm_mode = True


class UpdateClubEvent(BaseModel):
    event_name: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    description: Optional[str] = None
    image: Optional[str] = None

    class Config:
        orm_mode = True
