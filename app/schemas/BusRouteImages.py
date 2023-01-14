from typing import Optional

from pydantic import BaseModel


class BusRouteImageSchema(BaseModel):
    image: str
    ramadan_image: Optional[str] = None

    class Config:
        orm_mode = True


class CreateBusRouteImage(BaseModel):
    image: str
    ramadan_image: Optional[str] = None

    class Config:
        orm_mode = True


class BusRouteImageUpdate(BaseModel):
    image: str

    class Config:
        orm_mode = True


class BusRouteRamadanUpdate(BaseModel):
    ramadan_image: str

    class Config:
        orm_mode = True
