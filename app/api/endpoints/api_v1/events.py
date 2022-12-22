from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_current_student
from app.crud.crud_events import crudEvent
from app.db.database import get_db
from app.models import Events, User, EventOrganizer
from app.models.Student import Student
from app.schemas.Event import EventSchema, UpadteEvent

router = APIRouter()


@router.get('/get_All_Events')
async def get_events(*, db: Session = Depends(get_db), current_user: User.User = Depends(get_current_user)):
    return crudEvent.get_all_events(db=db)


@router.get('/get_all_events_students')
async def get_events_student(*, db: Session = Depends(get_db), current_user: Student = Depends(get_current_student)):
    return crudEvent.get_all_events(db=db)


@router.post('/create_Event')
async def create_event(*, db: Session = Depends(get_db), event_image: UploadFile = File(...),
                       event_in: EventSchema = Depends(), current_user: User.User = Depends(get_current_user)):
    extension = event_image.filename.split(".")[1]
    if extension not in ["png", "jpg", "jpeg", "gif"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="File extension not allowed")

    try:
        with open(f'static/images/Events/{event_image.filename}', 'wb') as f:
            while contents := event_image.file.read():
                f.write(contents)

        crudEvent.create_event(db=db, obj_in=event_in, image_name=event_image.filename, current_user=current_user.id,
                               organizers=event_in.organizers[0])

        return HTTPException(status_code=status.HTTP_200_OK, detail="Event Created Successfully")

    finally:
        event_image.file.close()


@router.delete('/delete_event{event_id}')
async def delete_event(*, db: Session = Depends(get_db), event_id: int,
                       current_user: User.User = Depends(get_current_user)):
    return crudEvent.delete_event_by_id(db=db, event_id=event_id)


@router.patch('/update_event/{id}')
async def update_event(*, db: Session = Depends(get_db), id: int, current_user: User.User = Depends(get_current_user),
                       obj_in: UpadteEvent = Depends(), event_image: UploadFile = File(...)):
    organizers = obj_in.organizers
    del obj_in.organizers
    db_obj = db.query(Events.Event).filter(Events.Event.event_id == id).update(values=obj_in.dict(exclude_none=True))
    db.commit()
    for i in organizers:
        db.query(EventOrganizer.EventOrganizer).filter(
            EventOrganizer.EventOrganizer.event_id == id).update(values={'organizer_id': i})
        db.commit()

    return db_obj
