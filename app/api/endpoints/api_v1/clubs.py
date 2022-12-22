from typing import List

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_current_student
from app.crud.crud_clubs import crudClubs
from app.crud.crud_event_club import crudEventClub
from app.db.database import get_db
from app.models import Club, Events
from app.models.User import User
from app.schemas.Event import ClubsEventSchema, ClubEventOut
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


@router.get('/get_club_events', response_model=list[ClubEventOut])
async def get_club_events(*, db: Session = Depends(get_db),
                          current_user: User = Depends(get_current_user)):
    return crudEventClub.get_clubs_events(db=db)


@router.get('/get_club_events_student', response_model=list[ClubEventOut])
async def get_club_events(*, db: Session = Depends(get_db),
                          current_user: User = Depends(get_current_student)):
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
async def create_club_event(*, db: Session = Depends(get_db), event_in: ClubsEventSchema = Depends(),
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
                                        current_user=current_user.id, organizers=event_in.organizers[0])

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


@router.delete('/delete_club_event/{event_id}')
async def delete_event(*, db: Session = Depends(get_db), event_id: int,
                       current_user: User = Depends(get_current_user)):
    event = db.query(Events.Event).filter(Events.Event.event_id == event_id)
    if event.first() is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Event Not Found")
    else:
        crudEventClub.delete_event_by_id(db=db, event_id=event_id)
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Event Club Deleted Successfully")


@router.patch('/update_club/{club_id}')
async def update_club(*, db: Session = Depends(get_db), club_id: int,
                      current_user: User = Depends(get_current_user), club_in: ClubUpdate = Depends(),
                      club_background_image: UploadFile = File(...),
                      club_icon_image: UploadFile = File(...)):
    db_obj = db.query(Club.Club).filter(Club.Club.club_id == club_id).update(values=club_in.dict(exclude_none=True))
    db.commit()
    return db_obj
