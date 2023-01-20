from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_current_student
from app.crud.crud_cso_event import crudCSOEvents
from app.db.database import get_db
from app.models import CSOEvents, User
from app.models.Student import Student
from app.schemas.CSOEvents import CreateCSOEvent

router = APIRouter()


@router.get('/get_All_CSO_Events')
async def get_cso_events(*, db: Session = Depends(get_db), current_user: User.User = Depends(get_current_user)):
    return db.query(CSOEvents.CSOEVENTS).all()


@router.get('/get_All_CSO_Events_Students')
async def get_cso_events_students(*, db: Session = Depends(get_db),
                                  current_user: Student = Depends(get_current_student)):
    return db.query(CSOEvents.CSOEVENTS).all()


@router.post('/create_cso_event')
async def create_cso_event(*, db: Session = Depends(get_db), obj_in: CreateCSOEvent = Depends(),
                           event_image: UploadFile = File(...), current_user: User.User = Depends(get_current_user)):
    extension = event_image.filename.split(".")[1]
    if extension not in ["png", "jpg", "jpeg"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="File extension not allowed")
    try:
        with open(f'static/images/CSOEvents/{event_image.filename}', 'wb') as f:
            while contents := event_image.file.read():
                f.write(contents)
        db = crudCSOEvents.create_club_event(db=db, obj_in=obj_in, image_name=event_image.filename,
                                             current_user=current_user.id)
        return db

    finally:
        event_image.file.close()
