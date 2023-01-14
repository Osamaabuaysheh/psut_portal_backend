from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.Student import Student
from app.models.Tutor import Tutor
from app.schemas.Tutor import TutorCreate, TutorUpdate


class CRUDTutor(CRUDBase[Tutor, TutorCreate, TutorUpdate]):
    def get_by_id(self, db: Session, *, tutor_id: int) -> Optional[Tutor]:
        return db.query(self.model).filter(Tutor.tutor_id == tutor_id).first()

    def get_by_company_name(self, db: Session, *, tutor_name: str) -> Optional[Tutor]:
        return db.query(self.model).filter(Tutor.tutor_name == tutor_name).first()

    def delete_tutor(self, db: Session, *, tutor_id: int):
        db_obj = db.query(self.model).filter(Tutor.tutor_id == tutor_id).delete()
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_tutor(self, db: Session, *, std_id: int, owner: id):
        student = db.query(Student).filter(Student.student_id == std_id).first()
        if student is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student doesn't exist")
        tutor = db.query(Tutor).filter(Tutor.student_id == student.student_id).first()
        if tutor is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tutor Already exist")
        db_obj = Tutor(
            student_id=student.student_id,
            owner_id=owner
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj


crudTutor = CRUDTutor(Tutor)
