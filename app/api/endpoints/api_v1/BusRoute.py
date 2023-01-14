from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_current_student
from app.crud.crud_bus_routes import crudBusRoute
from app.db.database import get_db
from app.models.BusRoute import BusRoute
from app.models.Student import Student
from app.models.User import User
from app.schemas.BusRoute import BusRouteOut

router = APIRouter()


@router.get('/get_All_Bus_Routes')
async def get_bus_routes(*, db: Session = Depends(get_db)):
    return db.query(BusRoute).all()


@router.get('/get_BusRouteByRouteName', response_model=list[BusRouteOut])
async def get_bus_routes_by_name(*, db: Session = Depends(get_db), route_name: str):
    bus_routes = crudBusRoute.get_by_name(db=db, bus_route_name=route_name)

    return bus_routes


@router.post('/upload_bus_routes')
async def upload_bus_route(*, db: Session = Depends(get_db),
                           current_user: User = Depends(get_current_user), file: UploadFile = File(...)):
    extension = file.filename.split(".")[1]
    if extension not in ["xlsx"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="File extension not allowed")

    try:
        with open(f"static/BusRoutes/{file.filename}", 'wb') as f:
            while contents := file.file.read():
                f.write(contents)

        return crudBusRoute.upload_bus_students(db=db, file=file)

    finally:
        file.file.close()


@router.post('/delete_all_bus_routes')
async def delete_all(*, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db.query(BusRoute).delete()
    db.commit()
    raise HTTPException(status_code=status.HTTP_200_OK, detail="Successfully Deleted All Routes")


@router.get('/get_route_details_by_student/{stdID}')
async def get_route_details_by_student(*, db: Session = Depends(get_db), stdID: int,
                                       current_user: Student = Depends(get_current_student)):
    routes = db.query(BusRoute).filter(BusRoute.student_id == stdID).first()
    if routes is not None:
        return routes
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="NOT FOUND")
