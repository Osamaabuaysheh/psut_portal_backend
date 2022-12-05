from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.CSOEvents import CSOEVENTS
from app.schemas.CSOEvents import CSOEventSchema, CreateCSOEvent


class CRUDCSOEvents(CRUDBase[CSOEVENTS, CSOEventSchema, CreateCSOEvent]):
    def get_club_event_name(self, db: Session, event_id: int):
        return db.query(CSOEVENTS).filter(CSOEVENTS.event_id == event_id).first()

    def get_cso_event_name(self, db: Session, *, event_name: str):
        return db.query(self.model).filter(CSOEVENTS.event_name == event_name).first()

    def create_club_event(self, db: Session, *, obj_in: CreateCSOEvent, image_name: str,
                          current_user: int):
        db_obj = CSOEVENTS(
            owner_id=current_user,
            event_name=obj_in.event_name,
            description=obj_in.description,
            end_time=obj_in.end_time,
            start_time=obj_in.start_time,
            end_date=obj_in.end_date,
            start_date=obj_in.start_date,
            location=obj_in.location,
            category=obj_in.category,
            gender=obj_in.gender,
            supervisor=obj_in.supervisor,
            hours_credit=obj_in.hours_credit,
            image=f'static/images/CSOEvents/{image_name}'
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


crudCSOEvents = CRUDCSOEvents(CSOEVENTS)
