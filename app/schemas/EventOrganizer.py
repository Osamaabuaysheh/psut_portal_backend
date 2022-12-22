from typing import Optional

from pydantic import BaseModel


class EventOrganizerSchema(BaseModel):
    event_id: Optional[int] = None
    organizer_id: Optional[int] = None

    class Config:
        orm_mode = True


class EventOrganizerCreate(BaseModel):
    event_id: int
    organizer_id: int

    class Config:
        orm_mode = True


class EventOrganizerUpadte(BaseModel):
    pass

    class Config:
        orm_mode = True
