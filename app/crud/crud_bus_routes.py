from typing import Optional, Any
import pandas as pd
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud import crudStudent
from app.crud.base import CRUDBase
from app.models.BusRoute import BusRoute
from app.schemas.BusRoute import BusRouteUpdate, CreateBusRoute


def validate_time(num: str) -> Any:
    x = num
    x = x[0] + x[1]
    if x.isnumeric():
        x = int(x)
        if x > 10:
            return x
        else:
            x = str(num)
            x = x[1]
            return int(x)
    else:
        return None


class CRUDBusRoutes(CRUDBase[BusRoute, CreateBusRoute, BusRouteUpdate]):
    def get_by_id(self, db: Session, *, bus_route_id: int) -> Optional[BusRoute]:
        return db.query(self.model).filter(BusRoute.club_id == bus_route_id).first()

    def get_by_name(self, db: Session, *, bus_route_name: str) -> list[BusRoute]:
        return db.query(self.model).filter(BusRoute.bus_route_name == bus_route_name).all()

    def get_all_separated_by_name(self, db: Session):
        return CRUDBase.get_multi(self, db=db)

    def upload_bus_students(self, db: Session, *, file):
        csv_reader = pd.read_excel(f"static/BusRoutes/{file.filename}")
        first = csv_reader.to_numpy()
        all_data = []
        for row in range(len(first)):
            data = {}
            for col in range(0, 9):
                data['mon_wed_back'] = validate_time(str(first[row][0]))
                data['mon_wed_presence'] = validate_time(str(first[row][1]))
                data['sun_tue_thu_back'] = validate_time(str(first[row][2]))
                data['sun_tue_thu_presence'] = validate_time(str(first[row][3]))
                data['pickup_dropoff'] = first[row][4]
                data['route'] = first[row][5]
                data['student_id'] = first[row][8]
            all_data.append(data)

        for index, data in enumerate(all_data):
            try:
                std = crudStudent.get_by_id(db=db, student_id=data['student_id'])
                if std is None:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student Doesn't Exist")
                bus_id = db.query(BusRoute).filter(data['student_id'] == BusRoute.student_id).first()
                if bus_id is not None:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Permit Already Exists")
                db_obj = BusRoute(
                    student_id=data['student_id'],
                    route=data['route'],
                    pickup_dropoff=data['pickup_dropoff'],
                    mon_wed_back=data['mon_wed_back'],
                    mon_wed_presence=data['mon_wed_presence'],
                    sun_tue_thu_back=data['sun_tue_thu_back'],
                    sun_tue_thu_presence=data['sun_tue_thu_presence']
                )
                db.add(db_obj)
                db.commit()
                db.refresh(db_obj)
            except:
                continue

        raise HTTPException(status_code=status.HTTP_200_OK, detail="Data Stored")


crudBusRoute = CRUDBusRoutes(BusRoute)
