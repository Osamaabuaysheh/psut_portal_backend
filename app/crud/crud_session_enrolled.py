from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.CourseSession import CourseSession
from app.models.SessionEnrolled import SessionEnrolled
from app.schemas.session_enrolled import SessionEnrolledCreate, SessionEnrolledUpdate, IncrementSession


class CRUDSessionEnrolled(CRUDBase[SessionEnrolled, SessionEnrolledCreate, SessionEnrolledUpdate]):
    def get_all_session_std(self, db: Session):
        sessions = db.query(CourseSession).all()
        total = {}
        for session in sessions:
            total[session.session_id] = db.query(self.model).where(session.session_id == self.model.sessionId).count()
        return total

    def increment_one_session(self, db: Session, obj_in: IncrementSession):
        db_obj = SessionEnrolled(
            student_id=obj_in.std_id,
            sessionId=obj_in.session_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # def delete_event_by_id(self, db: Session, *, permit_id: int):
    #     permit = db.query(self.model).filter(PermitHolders.permit_id == permit_id)
    #     if permit.first() is None:
    #         return permit
    #     else:
    #         permit.delete()
    #         db.commit()
    #         return "Event Deleted"
    #
    # def create_permit_holder(self, db: Session, *, obj_in: PermitHolderCreate, current_user: int):
    #     db_obj = PermitHolders(
    #         student_id=obj_in.student_id,
    #         permit_number=obj_in.permit_number,
    #         car_owner_name=obj_in.car_owner_name,
    #         car_type=obj_in.car_type,
    #         car_color=obj_in.car_color,
    #         phone_number=obj_in.phone_number,
    #         license_number=obj_in.license_number,
    #         owner_id=current_user
    #     )
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #
    #     return db_obj


crudSessionEnrolled = CRUDSessionEnrolled(SessionEnrolled)
