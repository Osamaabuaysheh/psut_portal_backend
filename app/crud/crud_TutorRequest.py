from typing import Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.TutorRequests import TutorRequests
from app.models.Student import Student
from app.schemas.TutorRequest import TutorRequestCreate, TutorRequestUpdate


class CRUDTutorRequest(CRUDBase[TutorRequests, TutorRequestCreate, TutorRequestUpdate]):
    def get_by_id(self, db: Session, *, tutorRequest_id: int) -> Optional[TutorRequests]:
        return db.query(self.model).filter(TutorRequests.tutor_request_id == tutorRequest_id).first()

    def create_request(self, db: Session, *, obj_in: TutorRequestCreate):
        tutor_name = db.query(Student).filter(obj_in.student_id == Student.student_id).first()
        db_obj = TutorRequests(
            semester_completion=obj_in.semster_completion,
            student_id=obj_in.student_id,
            course_id=obj_in.course_id,
            grade=obj_in.grade
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj


crudTutorRequest = CRUDTutorRequest(TutorRequests)
