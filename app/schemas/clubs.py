from pydantic import BaseModel
from typing import Optional


class ClubsSchema(BaseModel):
    club_id: Optional[int]
    club_name: Optional[str] = None
    club_image: Optional[str] = None
    club_icon_image: Optional[str] = None
    description: Optional[str] = None
    link: Optional[str] = None
    contact_info: Optional[str] = None

    class Config:
        orm_mode = True


class CreateClub(BaseModel):
    club_name: str
    description: str
    link: str
    contact_info: str


class ClubUpdate(ClubsSchema):
    pass
