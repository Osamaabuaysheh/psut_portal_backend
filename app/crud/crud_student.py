from typing import Optional

from sqlalchemy.orm import Session

from app.core import security
from app.crud.base import CRUDBase
from app.models.Student import Student
from app.models.StudentImages import StudentImages
from app.schemas.Student import StudentCreate
from app.schemas.User import UserCreate, UserUpdate


class CRUDStudent(CRUDBase[Student, UserCreate, UserUpdate]):
    def get_by_id(self, db: Session, *, student_id: int) -> Optional[Student]:
        return db.query(self.model).filter(Student.student_id == student_id).first()

    def get_by_email(self, db: Session, *, student_email: str) -> Optional[StudentImages]:
        return db.query(Student).filter(Student.email == student_email).first()

    def create_student(self, db: Session, *, obj_in: StudentCreate) -> Student:
        db_obj = Student(
            student_id=obj_in.student_id,
            email=obj_in.email,
            hashed_password=security.get_password_hash(obj_in.hashed_password),
            full_name=obj_in.full_name,
            colleage=obj_in.colleage,
            year=obj_in.year,
            student_image_id=obj_in.student_id,
            full_name_arabic=obj_in.full_name_arabic,
            hours_completed=obj_in.hours_completed)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


crudStudent = CRUDStudent(Student)
