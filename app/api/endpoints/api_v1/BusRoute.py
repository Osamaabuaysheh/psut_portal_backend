from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.crud.crud_bus_routes import crudBusRoute
from app.schemas.BusRoute import BusRouteOut, CreateBusRoute

router = APIRouter()


@router.get('/get_All_Bus_Routes')
async def get_bus_routes(*, db: Session = Depends(get_db)):
    routes = {}
    bus_routes_madina = crudBusRoute.get_by_name(db=db, bus_route_name='Madina')
    bus_routes_marj = crudBusRoute.get_by_name(db=db, bus_route_name='Marj Al-Hamam')
    bus_routes_radghdan = crudBusRoute.get_by_name(db=db, bus_route_name='Raghdan')
    routes['Madina'] = bus_routes_madina
    routes['Marj Al-Hamam'] = bus_routes_marj
    routes['Raghdan'] = bus_routes_radghdan

    return routes


@router.get('/get_BusRouteByRouteName', response_model=list[BusRouteOut])
async def get_bus_routes_by_name(*, db: Session = Depends(get_db), route_name: str):
    bus_routes = crudBusRoute.get_by_name(db=db, bus_route_name=route_name)

    return bus_routes


@router.post('/create_bus_route', response_model=BusRouteOut)
async def create_bus_routes(*, db: Session = Depends(get_db), create_obj: CreateBusRoute = Depends()):
    bus_routes = crudBusRoute.create_bus_route(db=db, obj_in=create_obj)

    return bus_routes
