from pydantic import BaseModel
from typing import Optional


class BusRouteSchema(BaseModel):
    bus_route_id: Optional[int]
    bus_route_name: Optional[str]
    first_route: Optional[str]
    second_route: Optional[str]
    third_route: Optional[str]
    fourth_route: Optional[str]
    location_trip: Optional[str]

    class Config:
        orm_mode = True


class CreateBusRoute(BaseModel):
    bus_route_name: str
    first_route: str
    second_route: str
    third_route: str
    fourth_route: Optional[str] = None
    location_trip: str

    class Config:
        orm_mode = True


class BusRouteOut(BaseModel):
    bus_route_name: str
    first_route: str
    second_route: str
    third_route: str
    fourth_route: Optional[str] = None
    location_trip: str

    class Config:
        orm_mode = True





class BusRouteUpdate(BusRouteSchema):
    pass
