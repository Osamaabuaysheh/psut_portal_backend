from typing import Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.CourseSession import CourseSession
from app.models.Tutor import Tutor
from app.schemas.courseSession import CreateCourseSession, UpdateCourseSession


class CRUDCourseSession(CRUDBase[CourseSession, CreateCourseSession, UpdateCourseSession]):
    def get_by_id(self, db: Session, *, course_session_id: int) -> Optional[CourseSession]:
        return db.query(CourseSession).filter(CourseSession.session_id == course_session_id).first()

    def get_by_name(self, db: Session, *, course_session_name: str) -> Optional[CourseSession]:
        return db.query(self.model).filter(CourseSession.course_name == course_session_name).first()

    def create_course_session(self, db: Session, *, obj_in: CreateCourseSession):
        tutor_id = db.query(Tutor).filter(Tutor.student_id == obj_in.student_id).first()

        course_obj = CourseSession(
            course_id=obj_in.course_id,
            tutor_id=tutor_id.tutor_id,
            start_time=obj_in.start_time,
            end_time=obj_in.end_time,
            day=obj_in.day
        )
        db.add(course_obj)
        db.commit()
        db.refresh(course_obj)
        return course_obj


crudCourseSession = CRUDCourseSession(CourseSession)
