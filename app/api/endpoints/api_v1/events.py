from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_current_student
from app.crud.crud_events import crudEvent
from app.db.database import get_db
from app.models import Events, User
from app.models.EventOrganizer import EventOrganizer
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

        raise HTTPException(status_code=status.HTTP_200_OK, detail="Event Created Successfully")

    finally:
        event_image.file.close()


@router.post('/delete_event{event_id}')
async def delete_event(*, db: Session = Depends(get_db), event_id: int,
                       current_user: User.User = Depends(get_current_user)):
    event = db.query(Events.Event).filter(Events.Event.event_id == event_id)
    if event.first() is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Event Doesn't Exist")
    else:
        crudEvent.delete_event_by_id(db=db, event_id=event_id)
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Event Deleted Successfully")


@router.post('/update_event/{id}')
async def update_event(*, db: Session = Depends(get_db), id: int, current_user: User.User = Depends(get_current_user),
                       obj_in: UpadteEvent = Depends(), event_image: UploadFile = None):
    if event_image is None:
        db.query(Events.Event).filter(Events.Event.event_id == id).update(
            values=obj_in.dict(exclude_none=True))
        db.commit()
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Event Updated Successfully")

    if event_image is not None:
        extension = event_image.filename.split(".")[1]
        if extension not in ["png", "jpg", "jpeg"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="File extension not allowed For Backgound")
        try:
            with open(f'static/images/Events/{event_image.filename}', 'wb') as f:
                while contents := event_image.file.read():
                    f.write(contents)
            obj_in.image = f'static/images/Events/{event_image.filename}'
            db.query(Events.Event).filter(Events.Event.event_id == id).update(
                values=obj_in.dict(exclude_none=True))
            db.commit()
            raise HTTPException(status_code=status.HTTP_200_OK, detail="Event Updated Successfully")
        finally:
            event_image.file.close()


@router.post('/add_organizer_event')
async def add_organizer_event(*, db: Session = Depends(get_db), event_id: int, org_id: int,
                              current_user: User.User = Depends(get_current_user)):
    eve_org = EventOrganizer(event_id=event_id, organizer_id=org_id)
    db.add(eve_org)
    db.commit()
    raise HTTPException(status_code=status.HTTP_200_OK, detail="Organizer added Successfully")


@router.post('/delete_eve_organizer')
async def delete_eve_org(*, db: Session = Depends(get_db), org_id: int, event_id: int,
                         current_user: User.User = Depends(get_current_user)):
    obj = db.query(EventOrganizer).filter(
        EventOrganizer.organizer_id == org_id and EventOrganizer.event_id == event_id).delete()
    db.commit()
    raise HTTPException(status_code=status.HTTP_200_OK, detail="Organizer Deleted Successfully")
