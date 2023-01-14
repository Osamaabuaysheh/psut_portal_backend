from typing import Optional

from pydantic import BaseModel


class ClubOrganizerSchema(BaseModel):
    event_id: Optional[int] = None
    organizer_id: Optional[int] = None

    class Config:
        orm_mode = True


class ClubOrganizerCreate(BaseModel):
    event_id: int
    organizer_id: int

    class Config:
        orm_mode = True


class ClubOrganizerUpadte(BaseModel):
    pass

    class Config:
        orm_mode = True
