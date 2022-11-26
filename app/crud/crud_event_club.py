from typing import Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.Club_Event import ClubEvent
from app.models.Events import Event
from app.models.Organizers import Organizer
from app.schemas.Event import ClubsEventSchema, ClubEventCreate


class CRUDEventClub(CRUDBase[ClubEvent, ClubsEventSchema, ClubEventCreate]):
    def get_clubs_events(self, db: Session):
        return db.query(Event).filter(ClubEvent.event_id == Event.event_id).all()

    def get_club_event_name(self, db: Session, event_id: int):
        return db.query(ClubEvent).filter(ClubEvent.event_id == event_id).first()

    def get_club_name(self, db: Session, *, club_name: str):
        return db.query(self.model).filter(ClubEvent.club_name == club_name.lower()).first()

    def create_club_event(self, db: Session, *, obj_in: ClubsEventSchema, image_name: str, organizers_images: list,
                          current_user: int):
        db_obj = Event(
            event_name=obj_in.event_name,
            start_date=obj_in.start_date,
            end_date=obj_in.end_date,
            start_time=obj_in.start_time,
            end_time=obj_in.end_time,
            location=obj_in.location,
            description=obj_in.description,
            image=f'static/images/Events/{image_name}',
            owner_id=current_user
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        obj_in.organizers = obj_in.organizers[0].split(',')
        for i in range(len(obj_in.organizers)):
            db_obj_organizers = Organizer(organizer_image=f'static/images/Organizers/{organizers_images[i]}',
                                          event_id=db_obj.event_id,
                                          organizer_name=obj_in.organizers[i])
            db.add(db_obj_organizers)
            db.commit()
            db.refresh(db_obj_organizers)
        club_db_obj = ClubEvent(
            club_name=obj_in.club_name.lower(),
            event_id=db_obj.event_id
        )
        db.add(club_db_obj)
        db.commit()
        db.refresh(club_db_obj)
        return db_obj


crudEventClub = CRUDEventClub(ClubEvent)
