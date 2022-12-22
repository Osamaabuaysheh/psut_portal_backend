from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.Organizers import Organizer
from app.schemas.organizer import OrganizerSchema, OrganizerCreate


class CRUDOrganzier(CRUDBase[Organizer, OrganizerSchema, OrganizerCreate]):
    def create_organizer(self, db: Session, *, obj_in: OrganizerCreate, image_name):
        db_obj = Organizer(
            organizer_name=obj_in.organizer_name,
            organizer_image=f'static/images/Organizers/{image_name}'
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj


crudOrganizer = CRUDOrganzier(Organizer)
