from typing import Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.Tutor import Tutor
from app.models.Student import Student
from app.schemas.Tutor import TutorCreate, TutorUpdate


class CRUDTutor(CRUDBase[Tutor, TutorCreate, TutorUpdate]):
    def get_by_id(self, db: Session, *, tutor_id: int) -> Optional[Tutor]:
        return db.query(self.model).filter(Tutor.tutor_id == tutor_id).first()

    def get_by_company_name(self, db: Session, *, tutor_name: str) -> Optional[Tutor]:
        return db.query(self.model).filter(Tutor.tutor_name == tutor_name).first()

    def create_tutor(self, db: Session, *, obj_in: TutorCreate, owner: id):
        tutor_name = db.query(Student).filter(obj_in.student_id == Student.student_id).first()
        db_obj = Tutor(
            tutor_name=tutor_name.full_name,
            student_id=obj_in.student_id,
            gpa=obj_in.gpa,
            year=obj_in.year,
            owner_id=owner
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj


crudTutor = CRUDTutor(Tutor)
