from typing import Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.BusRoute import BusRoute
from app.schemas.BusRoute import BusRouteUpdate, CreateBusRoute


class CRUDBusRoutes(CRUDBase[BusRoute, CreateBusRoute, BusRouteUpdate]):
    def get_by_id(self, db: Session, *, bus_route_id: int) -> Optional[BusRoute]:
        return db.query(self.model).filter(BusRoute.club_id == bus_route_id).first()

    def get_by_name(self, db: Session, *, bus_route_name: str) -> list[BusRoute]:
        return db.query(self.model).filter(BusRoute.bus_route_name == bus_route_name).all()

    def get_all_separated_by_name(self, db: Session):
        return CRUDBase.get_multi(self, db=db)

    def create_bus_route(self, db: Session, *, obj_in: CreateBusRoute):
        db_obj = BusRoute(
            location_trip=obj_in.location_trip,
            first_route=obj_in.first_route,
            second_route=obj_in.second_route,
            third_route=obj_in.third_route,
            fourth_route=obj_in.fourth_route,
            bus_route_name=obj_in.bus_route_name
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj


crudBusRoute = CRUDBusRoutes(BusRoute)
