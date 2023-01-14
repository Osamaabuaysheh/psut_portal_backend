from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.Club import Club
from app.models.ClubOrganizer import ClubOrganizer
from app.models.Club_Event import ClubEvent
from app.models.Events import Event
from app.models.User import User
from app.schemas.Event import ClubsEventSchema, ClubEventCreate


class CRUDEventClub(CRUDBase[ClubEvent, ClubsEventSchema, ClubEventCreate]):
    def get_clubs_events(self, db: Session):
        events = db.query(Event).filter(ClubEvent.event_id == Event.event_id).all()
        for event in events:
            orgs = []
            org = db.query(Club).filter(
                ClubOrganizer.event_id == event.event_id).filter(ClubOrganizer.organizer_id == Club.club_id).all()
            for i in org:
                obj = {"organizer_image": i.club_image,
                       "organizer_id": i.club_id,
                       "organizer_name": i.club_name}
                orgs.append(obj)
            club = db.query(Club).filter(
                Club.club_id == ClubEvent.club_id and event.event_id == ClubEvent.event_id).first()
            owner = db.query(User).filter(User.id == event.owner_id).first()
            event = event.__dict__
            event['organizers'] = orgs
            event['club_name'] = club.club_name
            event['owner_role'] = owner.user_role
        return events

    def get_club_event_name(self, db: Session, event_id: int):
        return db.query(ClubEvent).filter(ClubEvent.event_id == event_id).first()

    def delete_event_by_id(self, db: Session, event_id: int):
        db_obj = db.query(Event).filter(Event.event_id == event_id).delete()
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_club_name(self, db: Session, *, club_name: str):
        return db.query(self.model).filter(ClubEvent.club_name == club_name.lower()).first()

    def create_club_event(self, db: Session, *, obj_in: ClubEventCreate, image_name: str, current_user: int,
                          organizers):
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

        db_obj_organizer_event = ClubOrganizer(event_id=db_obj.event_id, organizer_id=obj_in.club_organizer)
        db.add(db_obj_organizer_event)
        db.commit()
        db.refresh(db_obj_organizer_event)
        club = db.query(Club).filter(Club.club_id == obj_in.club_organizer).first()
        club_db_obj = ClubEvent(
            club_id=club.club_id,
            event_id=db_obj.event_id
        )
        db.add(club_db_obj)
        db.commit()
        db.refresh(club_db_obj)
        return db_obj


crudEventClub = CRUDEventClub(ClubEvent)
