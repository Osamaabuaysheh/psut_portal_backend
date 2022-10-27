from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status, Body, Request, Form
from sqlalchemy.orm import Session
from typing import List
from datetime import date, time
from app.db.database import get_db
from app.models import Events, Organizers
from app.schemas.Event import EventOut, CreateEvent, EventSchema
from app.schemas.organizer import OrganizerSchema, OrganizerOut, OrgOut
from app.crud.crud_events import crudEvent

router = APIRouter()


@router.get('/get_All_Events', response_model=List[EventOut])
async def get_events(*, db: Session = Depends(get_db)):
    events = db.query(Events.Event).all()
    for event in events:
        org = db.query(Organizers.Organizer).where(event.event_id == Organizers.Organizer.event_id).all()
        event = event.__dict__
        event['organizers'] = org

    return events


@router.post('/create_Event')
async def create_event(*, db: Session = Depends(get_db), event_image: UploadFile = File(...),
                       organizers_images: list[UploadFile] = File(...),
                       event_in: EventSchema = Depends()):
    extension = event_image.filename.split(".")[1]
    if extension not in ["png", "jpg", "jpeg"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="File extension not allowed")

    for org_image in organizers_images:
        extension_orgaanizer_image = org_image.filename.split(".")[1]
        if extension_orgaanizer_image not in ["png", "jpg", "jpeg"]:
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
                               organizers_images=org_images)

        return "Event Created Successfully"

    finally:
        event_image.file.close()
        for org_image in organizers_images:
            org_image.file.close()
