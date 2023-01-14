from typing import Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.Course import Course
from app.models.CourseSession import CourseSession
from app.models.Student import Student
from app.models.Tutor import Tutor
from app.schemas.courseSession import CreateCourseSession, UpdateCourseSession


class CRUDCourseSession(CRUDBase[CourseSession, CreateCourseSession, UpdateCourseSession]):
    def get_by_id(self, db: Session, *, course_session_id: int) -> Optional[CourseSession]:
        return db.query(CourseSession).filter(CourseSession.session_id == course_session_id).first()

    def delete_session(self, db: Session, *, course_session_id: int):
        session = db.query(CourseSession).filter(CourseSession.session_id == course_session_id).delete()
        db.commit()
        db.refresh(session)
        return session

    def get_course_session_details(self, db: Session):
        courseSessions = db.query(CourseSession.course_id).group_by(
            CourseSession.course_id).all()
        all = []
        for courseSession in courseSessions:
            sessions = db.query(CourseSession).filter(CourseSession.course_id == courseSession.course_id).all()
            tutor_id = db.query(CourseSession).filter(
                CourseSession.course_id == courseSession.course_id).first().tutor_id
            std_id = db.query(Tutor).filter(Tutor.tutor_id == tutor_id).first().student_id
            std_name = db.query(Student).filter(Student.student_id == std_id).first().full_name
            obj = {'course_id': courseSession.course_id, 'sessions': sessions,
                   'course_name': db.query(Course).filter(
                       courseSession.course_id == Course.course_id).first().course_name,
                   'std_name': std_name, 'std_id': std_id, 'tutor_id': tutor_id}
            all.append(obj)

        return all

    def get_by_name(self, db: Session, *, course_session_name: str) -> Optional[CourseSession]:
        return db.query(self.model).filter(CourseSession.course_name == course_session_name).first()

    def create_course_session(self, db: Session, *, obj_in: CreateCourseSession):
        tutor_id = db.query(Tutor).filter(Tutor.tutor_id == obj_in.tutor_id).first()

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
