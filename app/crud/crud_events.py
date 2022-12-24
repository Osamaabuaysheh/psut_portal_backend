from typing import Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.EventOrganizer import EventOrganizer
from app.models.Events import Event
from app.models.Organizers import Organizer
from app.models.User import User
from app.schemas.Event import CreateEvent, EventOut


class CRUDEvents(CRUDBase[Event, CreateEvent, EventOut]):
    def get_all_events(self, db: Session) -> Optional[list[Event]]:
        events = db.query(Event).all()
        for event in events:
            org = db.query(Organizer).filter(
                EventOrganizer.event_id == event.event_id).filter(
                EventOrganizer.organizer_id == Organizer.organizer_id).all()
            owner = db.query(User).filter(User.id == event.owner_id).first()
            event = event.__dict__
            event['organizers'] = org
            event['owner_role'] = owner.user_role
        return events

    def get_by_id(self, db: Session, *, event_id: int) -> Optional[Event]:
        return db.query(self.model).filter(Event.event_id == event_id).first()

    def get_image_name(self, db: Session, *, image_name: str):
        return db.query(self.model).filter(Event.image == image_name).first()

    def delete_event_by_id(self, db: Session, *, event_id: int):
        event = db.query(self.model).filter(Event.event_id == event_id)
        if event.first() is None:
            return event
        else:
            event.delete()
            db.commit()
            db.refresh(event)
            return "Event Deleted"

    def create_event(self, db: Session, *, obj_in: CreateEvent, image_name: str, organizers,
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
        obj_in.organizers = organizers.split(',')
        for i in obj_in.organizers:
            db_obj_organizers_events = EventOrganizer(event_id=db_obj.event_id, organizer_id=i)
            db.add(db_obj_organizers_events)
            db.commit()
            db.refresh(db_obj_organizers_events)

        return db_obj


crudEvent = CRUDEvents(Event)
