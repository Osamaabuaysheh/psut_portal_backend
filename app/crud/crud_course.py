from typing import Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.Course import Course
from app.models.course_tutor import CourseTutor
from app.schemas.Course import CreateCourse, UpdateCourse
from app.models.Tutor import Tutor
from app.models.CourseSession import CourseSession


class CRUDCourse(CRUDBase[Course, CreateCourse, UpdateCourse]):
    def get_by_id(self, db: Session, *, course_id: int) -> Optional[Course]:
        return db.query(self.model).filter(Course.course_id == course_id).first()

    def get_by_name(self, db: Session, *, course_name: str) -> Optional[Course]:
        return db.query(self.model).filter(Course.course_name == course_name).first()

    def get_course_details(self, db: Session):
        courses = db.query(Course).all()
        all_courses = []
        for course in courses:
            course_sessions = db.query(CourseSession).filter(
                course.course_id == CourseSession.course_id).all()
            course_tutors = db.query(Tutor).filter(CourseTutor.course_id == course.course_id,
                                                   Tutor.tutor_id == CourseTutor.tutor_id).first()
            course = course.__dict__
            course['sessions'] = course_sessions
            course['Tutor'] = course_tutors
            all_courses.append(course)
        return all_courses

    def create_course(self, db: Session, *, obj_in: CreateCourse):
        course_obj = Course(
            course_id=obj_in.course_id,
            course_name=obj_in.course_name,
            college=obj_in.college
        )
        db.add(course_obj)
        db.commit()
        db.refresh(course_obj)

        tutor_id = db.query(Tutor).filter(Tutor.student_id == obj_in.student_id).first()
        if tutor_id.tutor_id:
            coursr_tutor_obj = CourseTutor(
                course_id=obj_in.course_id,
                tutor_id=tutor_id.tutor_id
            )
            db.add(coursr_tutor_obj)
            db.commit()
            db.refresh(coursr_tutor_obj)
        return course_obj


crudCourse = CRUDCourse(Course)
