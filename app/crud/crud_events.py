from typing import Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.Events import Event
from app.models.Organizers import Organizer
from app.schemas.Event import CreateEvent, EventOut


class CRUDEvents(CRUDBase[Event, CreateEvent, EventOut]):
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
            return "Event Deleted"

    def create_event(self, db: Session, *, obj_in: CreateEvent, image_name: str, organizers_images: list,
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

        return db_obj


crudEvent = CRUDEvents(Event)
