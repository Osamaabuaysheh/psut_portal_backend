from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.crud.crud_clubs import crudClubs
from app.crud.crud_event_club import crudEventClub
from app.schemas.clubs import ClubsSchema, CreateClub
from app.schemas.Event import ClubsEventSchema, ClubEventOut
from app.api.deps import get_current_user
from app.models.User import User
from app.models import Organizers

router = APIRouter()


@router.get('/get_All_Clubs', response_model=List[ClubsSchema])
async def get_clubs(*, db: Session = Depends(get_db)):
    clubs = crudClubs.get_multi(db=db)

    return clubs


@router.get('/get_club_by_name{club_name}', response_model=ClubsSchema)
async def get_club_by_name(*, db: Session = Depends(get_db), club_name: str):
    club = crudClubs.get_by_name(db=db, club_name=club_name)

    return club


@router.post('/create_club', response_model=ClubsSchema)
async def create_club(*, db: Session = Depends(get_db), club_background_image: UploadFile = File(...),
                      club_icon_image: UploadFile = File(...),
                      club_in: CreateClub = Depends()):
    extension = club_background_image.filename.split(".")[1]
    if extension not in ["png", "jpg", "jpeg"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="File extension not allowed For Backgound")

    club_extension_icon = club_icon_image.filename.split(".")[1]
    if club_extension_icon not in ["png", "jpg", "jpeg"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="File extension not allowed For Icon")

    try:
        with open(f'static/images/Clubs/backgroundImage/{club_background_image.filename}', 'wb') as f:
            while contents := club_background_image.file.read():
                f.write(contents)
        with open(f'static/images/Clubs/IconImages/{club_icon_image.filename}', 'wb') as f:
            while contents := club_icon_image.file.read():
                f.write(contents)

        db_obj = crudClubs.create_club(db=db, obj_in=club_in, club_icon_image=club_icon_image.filename,
                                       club_background_image=club_background_image.filename)
        return db_obj
    finally:
        club_background_image.file.close()
        club_icon_image.file.close()


@router.post('/create_Event_Club')
async def create_club_event(*, db: Session = Depends(get_db), event_in: ClubsEventSchema = Depends(),
                            event_image: UploadFile = File(...),
                            organizers_images: list[UploadFile] = File(...)
                            , current_user: User = Depends(get_current_user)
                            ):
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

        crudEventClub.create_club_event(db=db, obj_in=event_in, image_name=event_image.filename,
                                        organizers_images=org_images, current_user=current_user.id)

        return "Event Created Successfully"

    finally:
        event_image.file.close()
        for org_image in organizers_images:
            org_image.file.close()


@router.get('/get_club_events', response_model=list[ClubEventOut])
async def get_club_events(*, db: Session = Depends(get_db)):
    events = crudEventClub.get_clubs_events(db=db)
    for event in events:
        org = db.query(Organizers.Organizer).where(event.event_id == Organizers.Organizer.event_id).all()
        club = crudEventClub.get_club_event_name(db=db, event_id=event.event_id)
        event = event.__dict__
        event['organizers'] = org
        event['club_name'] = club.club_name

    return events
