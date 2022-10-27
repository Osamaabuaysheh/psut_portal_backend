from pydantic import BaseModel
from typing import Optional


class OrganizerSchema(BaseModel):
    organizer_name: str
    organizer_image: Optional[str]

    class Config:
        orm_mode = True


class OrganizerOut(BaseModel):
    oragainzer_id: int
    oragainzer_name: str
    organizer_image: str

    class Config:
        orm_mode = True


class OrgOut(BaseModel):
    orga: list[OrganizerSchema]

    class Config:
        orm_mode = True
