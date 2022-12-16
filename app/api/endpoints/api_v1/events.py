from typing import List

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.crud.crud_events import crudEvent
from app.db.database import get_db
from app.models import Events, Organizers, User
from app.schemas.Event import EventOut, EventSchema

router = APIRouter()


@router.get('/get_All_Events', response_model=List[EventOut])
async def get_events(*, db: Session = Depends(get_db)):
    events = db.query(Events.Event).all()
    for event in events:
        org = db.query(Organizers.Organizer).where(event.event_id == Organizers.Organizer.event_id).all()
        owner = db.query(User.User).filter(User.User.id == event.owner_id).first()
        event = event.__dict__
        event['organizers'] = org
        event['owner_role'] = owner.user_role

    return events


@router.post('/create_Event')
async def create_event(*, db: Session = Depends(get_db), event_image: UploadFile = File(...),
                       organizers_images: list[UploadFile] = File(...),
                       event_in: EventSchema = Depends(), current_user: User.User = Depends(get_current_user)):
    extension = event_image.filename.split(".")[1]
    if extension not in ["png", "jpg", "jpeg", "gif"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="File extension not allowed")

    for org_image in organizers_images:
        extension_orgaanizer_image = org_image.filename.split(".")[1]
        if extension_orgaanizer_image not in ["png", "jpg", "jpeg", "gif"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,

                                detail="File extension not allowed")

    try:
        with open(f'static/images/Events/{event_image.filename}', 'wb') as f:
            while contents := event_image.file.read():
                f.write(contents)
        for org_image in organizers_images:
            with open(f'static/images/Organizers/{org_image.filename}', 'wb') as f:
                while contents := org_image.file.read():
                    f.write(contents)

        org_images = []
        for image in organizers_images:
            org_images.append(image.filename)

        crudEvent.create_event(db=db, obj_in=event_in, image_name=event_image.filename,
                               organizers_images=org_images, current_user=current_user.id)

        return "Event Created Successfully"

    finally:
        event_image.file.close()
        for org_image in organizers_images:
            org_image.file.close()


@router.post('/delete_event{event_id}')
async def delete_event(*, db: Session = Depends(get_db), event_id: int,
                       current_user: User.User = Depends(get_current_user)):
    return crudEvent.delete_event_by_id(db=db, event_id=event_id)
