from typing import List

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_current_student
from app.crud.crud_clubs import crudClubs
from app.crud.crud_event_club import crudEventClub
from app.db.database import get_db
from app.models import Club, Events
from app.models.ClubOrganizer import ClubOrganizer
from app.models.Student import Student
from app.models.User import User
from app.schemas.Event import ClubEventCreate, UpdateClubEvent
from app.schemas.clubs import ClubsSchema, CreateClub, ClubUpdate

router = APIRouter()


@router.get('/get_All_Clubs', response_model=List[ClubsSchema])
async def get_clubs(*, db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    clubs = crudClubs.get_multi(db=db)

    return clubs


@router.get('/get_All_Clubs_Student', response_model=List[ClubsSchema])
async def get_clubs_student(*, db: Session = Depends(get_db),
                            current_user: User = Depends(get_current_student)):
    clubs = crudClubs.get_multi(db=db)

    return clubs


@router.get('/get_club_by_name{club_name}', response_model=ClubsSchema)
async def get_club_by_name(*, db: Session = Depends(get_db), club_name: str,
                           current_user: User = Depends(get_current_user)):
    club = crudClubs.get_by_name(db=db, club_name=club_name)

    return club


@router.get('/get_club_events')
async def get_club_events(*, db: Session = Depends(get_db),
                          current_user: User = Depends(get_current_user)):
    return crudEventClub.get_clubs_events(db=db)


@router.get('/get_club_events_student')
async def get_club_events(*, db: Session = Depends(get_db),
                          current_user: Student = Depends(get_current_student)):
    return crudEventClub.get_clubs_events(db=db)


@router.post('/create_club', response_model=ClubsSchema)
async def create_club(*, db: Session = Depends(get_db), club_background_image: UploadFile = File(...),
                      club_icon_image: UploadFile = File(...),
                      club_in: CreateClub = Depends(),
                      current_user: User = Depends(get_current_user)):
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
async def create_club_event(*, db: Session = Depends(get_db), event_in: ClubEventCreate = Depends(),
                            event_image: UploadFile = File(...), current_user: User = Depends(get_current_user)
                            ):
    extension = event_image.filename.split(".")[1]
    if extension not in ["png", "jpg", "jpeg"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="File extension not allowed")

    try:
        with open(f'static/images/Events/{event_image.filename}', 'wb') as f:
            while contents := event_image.file.read():
                f.write(contents)

        crudEventClub.create_club_event(db=db, obj_in=event_in, image_name=event_image.filename,
                                        current_user=current_user.id, organizers=event_in.club_organizer)

        return "Event Created Successfully"

    finally:
        event_image.file.close()


@router.delete('/delete_club/{club_id}')
async def delete_event(*, db: Session = Depends(get_db), club_id: int,
                       current_user: User = Depends(get_current_user)):
    club = db.query(Club.Club).filter(Club.Club.club_id == club_id)
    if club.first() is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Club Not Found")
    else:
        crudClubs.delete_club_by_id(db=db, club_id=club_id)
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Club Deleted Successfully")


@router.post('/delete_club_event/{event_id}')
async def delete_event(*, db: Session = Depends(get_db), event_id: int,
                       current_user: User = Depends(get_current_user)):
    event = db.query(Events.Event).filter(Events.Event.event_id == event_id)
    if event.first() is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Event Not Found")
    else:
        crudEventClub.delete_event_by_id(db=db, event_id=event_id)
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Event Club Deleted Successfully")


@router.post('/update_club/{club_id}')
async def update_club(*, db: Session = Depends(get_db), club_id: int,
                      current_user: User = Depends(get_current_user), club_in: ClubUpdate = Depends(),
                      club_background_image: UploadFile = None,
                      club_icon_image: UploadFile = None):
    if club_background_image is not None and club_icon_image is not None:
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
            club_in.club_icon_image = f'static/images/Clubs/IconImages/{club_icon_image.filename}'
            club_in.club_image = f'static/images/Clubs/backgroundImage/{club_background_image.filename}'
            db_obj = db.query(Club.Club).filter(Club.Club.club_id == club_id).update(
                values=club_in.dict(exclude_none=True))
            db.commit()
            return db_obj
        finally:
            club_background_image.file.close()
            club_icon_image.file.close()

    if club_background_image is None and club_icon_image is None:
        db_obj = db.query(Club.Club).filter(Club.Club.club_id == club_id).update(
            values=club_in.dict(exclude_none=True))
        db.commit()
        return db_obj
    if club_background_image is None and club_icon_image is not None:
        club_extension_icon = club_icon_image.filename.split(".")[1]
        if club_extension_icon not in ["png", "jpg", "jpeg"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="File extension not allowed For Icon")
        try:
            with open(f'static/images/Clubs/IconImages/{club_icon_image.filename}', 'wb') as f:
                while contents := club_icon_image.file.read():
                    f.write(contents)
            club_in.club_icon_image = f'static/images/Clubs/IconImages/{club_icon_image.filename}'
            db_obj = db.query(Club.Club).filter(Club.Club.club_id == club_id).update(
                values=club_in.dict(exclude_none=True))
            db.commit()
            return db_obj
        finally:
            club_icon_image.file.close()
    if club_background_image is not None and club_icon_image is None:
        extension = club_background_image.filename.split(".")[1]
        if extension not in ["png", "jpg", "jpeg"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="File extension not allowed For Backgound")
    try:
        with open(f'static/images/Clubs/backgroundImage/{club_background_image.filename}', 'wb') as f:
            while contents := club_background_image.file.read():
                f.write(contents)

        club_in.club_image = f'static/images/Clubs/backgroundImage/{club_background_image.filename}'
        db_obj = db.query(Club.Club).filter(Club.Club.club_id == club_id).update(
            values=club_in.dict(exclude_none=True))
        db.commit()
        return db_obj
    finally:
        club_background_image.file.close()


@router.post('/update_club_event/{id}')
async def update_club_event(*, db: Session = Depends(get_db), id: int,
                            current_user: User = Depends(get_current_user),
                            obj_in: UpdateClubEvent = Depends(), event_image: UploadFile = None):
    if event_image is None and obj_in.organizers[0] == '':
        del obj_in.organizers
        db.query(Events.Event).filter(Events.Event.event_id == id).update(
            values=obj_in.dict(exclude_none=True))
        db.commit()
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Event Updated Successfully")
    if event_image is None:
        if obj_in.organizers[0] != '':
            organizers = obj_in.organizers[0].split(',')
            del obj_in.organizers
            db.query(Events.Event).filter(Events.Event.event_id == id).update(
                values=obj_in.dict(exclude_none=True))
            db.commit()
            for i in organizers:
                db.query(ClubOrganizer).filter(ClubOrganizer.event_id == id).update(values={'organizer_id': i})
                db.commit()
            raise HTTPException(status_code=status.HTTP_200_OK, detail="Event Updated Successfully")
    if obj_in.organizers is None:
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

    extension = event_image.filename.split(".")[1]
    if extension not in ["png", "jpg", "jpeg"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="File extension not allowed For Backgound")
    try:
        with open(f'static/images/Events/{event_image.filename}', 'wb') as f:
            while contents := event_image.file.read():
                f.write(contents)
        obj_in.image = f'static/images/Events/{event_image.filename}'
        organizers = obj_in.organizers[0].split(',')
        del obj_in.organizers
        db.query(Events.Event).filter(Events.Event.event_id == id).update(
            values=obj_in.dict(exclude_none=True))
        db.commit()
        for i in organizers:
            db.query(ClubOrganizer).filter(ClubOrganizer.event_id == id).update(values={'organizer_id': i})
            db.commit()
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Event Updated Successfully")
    finally:
        event_image.file.close()


@router.post('/add_club_organizer_event')
async def add_club_organizer_event(*, db: Session = Depends(get_db), event_id: int, org_id: int,
                                   current_user: User = Depends(get_current_user)):
    eve_org = ClubOrganizer(event_id=event_id, organizer_id=org_id)
    db.add(eve_org)
    db.commit()
    raise HTTPException(status_code=status.HTTP_200_OK, detail="Organizer added Successfully")


@router.post('/delete_club_organizer_event')
async def delete__club_eve_org(*, db: Session = Depends(get_db), org_id: int, event_id: int,
                         current_user: User = Depends(get_current_user)):
    obj = db.query(ClubOrganizer).filter(
        ClubOrganizer.organizer_id == org_id and ClubOrganizer.event_id == event_id).delete()
    db.commit()
    raise HTTPException(status_code=status.HTTP_200_OK, detail="Organizer Deleted Successfully")
