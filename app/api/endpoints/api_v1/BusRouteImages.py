from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_current_student
from app.db.database import get_db
from app.models.BusRouteImages import BusRouteImages
from app.models.Student import Student
from app.models.User import User

router = APIRouter()


@router.get('/get_All_Bus_Routes_Images')
async def get_clubs(*, db: Session = Depends(get_db),
                    current_user: Student = Depends(get_current_student)):
    return db.query(BusRouteImages).first()


@router.post('/upload_image_bus_route')
async def get_jobs(*, db: Session = Depends(get_db), bus_image: UploadFile = File(...),
                   current_user: User = Depends(get_current_user)):
    extension = bus_image.filename.split(".")[1]
    if extension not in ["png", "jpg", "jpeg"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="File extension not allowed For Backgound")

    try:
        with open(f'static/images/BusRouteImages/{bus_image.filename}', 'wb') as f:
            while contents := bus_image.file.read():
                f.write(contents)
        image = db.query(BusRouteImages).first()
        if image is None:
            db_obj = BusRouteImages(
                image=f'static/images/BusRouteImages/{bus_image.filename}'
            )
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        else:
            db.query(BusRouteImages).filter(BusRouteImages.id == image.id).update(
                values={'image': f'static/images/BusRouteImages/{bus_image.filename}'})
            db.commit()
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Image Uploaded Successfully")
    finally:
        bus_image.file.close()


@router.post('/upload_image_bus_route_ramadan')
async def get_jobs(*, db: Session = Depends(get_db), bus_image: UploadFile = File(...),
                   current_user: User = Depends(get_current_user)):
    extension = bus_image.filename.split(".")[1]
    if extension not in ["png", "jpg", "jpeg"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="File extension not allowed For Backgound")

    try:
        with open(f'static/images/BusRouteImages/{bus_image.filename}', 'wb') as f:
            while contents := bus_image.file.read():
                f.write(contents)
        image = db.query(BusRouteImages).first()
        if image is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please Upload Bus route Image First")

        db.query(BusRouteImages).filter(BusRouteImages.id == image.id).update(
            values={'ramadan_image': f'static/images/BusRouteImages/{bus_image.filename}'})
        db.commit()
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Image Uploaded Successfully")
    finally:
        bus_image.file.close()
