from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.EventOrganizer import EventOrganizer
from app.schemas.EventOrganizer import EventOrganizerSchema, EventOrganizerCreate


class CRUDEventOrganzier(CRUDBase[EventOrganizer, EventOrganizerSchema, EventOrganizerCreate]):
    def create_event_organizer(self, db: Session, *, obj_in: EventOrganizerCreate):
        db_obj = EventOrganizer(
            event_id=obj_in.event_id,
            organizer_id=obj_in.organizer_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj


crudEventOrganizer = CRUDEventOrganzier(EventOrganizer)
