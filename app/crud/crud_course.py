from typing import Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.Course import Course
from app.models.CourseSession import CourseSession
from app.models.SessionEnrolled import SessionEnrolled
from app.models.Student import Student
from app.models.StudentImages import StudentImages
from app.models.Tutor import Tutor
from app.models.course_tutor import CourseTutor
from app.schemas.Course import CreateCourse, UpdateCourse


class CRUDCourse(CRUDBase[Course, CreateCourse, UpdateCourse]):
    def get_by_id(self, db: Session, *, course_id: int) -> Optional[Course]:
        return db.query(self.model).filter(Course.course_id == course_id).first()

    def get_by_name(self, db: Session, *, course_name: str) -> Optional[Course]:
        return db.query(self.model).filter(Course.course_name == course_name).first()

    def delete_course(self, db: Session, *, course_id: int):
        db_obj = db.query(self.model).filter(Course.course_id == course_id).delete()
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_course_details(self, db: Session):
        sessions = db.query(CourseSession.tutor_id, CourseSession.course_id).group_by(CourseSession.tutor_id,
                                                                                      CourseSession.course_id).all()

        total_sessions = []
        for session in sessions:
            std_id = db.query(Tutor).filter(session.tutor_id == Tutor.tutor_id).first().student_id
            student = db.query(Student).filter(std_id == Student.student_id).first()
            image = db.query(StudentImages).filter(StudentImages.id == student.student_image_id).first().imagePath
            course = db.query(Course).filter(session.course_id == Course.course_id).first()
            all_sessions = db.query(CourseSession).filter(session.course_id == CourseSession.course_id).filter(
                CourseSession.tutor_id == session.tutor_id).all()
            for se in all_sessions:
                total = db.query(SessionEnrolled).where(
                    se.session_id == SessionEnrolled.sessionId).count()
                se = se.__dict__
                se['total'] = total
            item = {
                "tutor_name": student.full_name,
                "tutor_image": image,
                "course_name": course.course_name,
                "course_id": session.course_id,
                "college": course.college,
                "sessions": all_sessions
            }
            total_sessions.append(item)

        return total_sessions


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

# courses = db.query(Course).all()
#         all_courses = []
#         sessions = db.query(CourseSession).all()
#         for session in sessions:
#             total = db.query(SessionEnrolled.SessionEnrolled).where(
#                 session.session_id == SessionEnrolled.SessionEnrolled.sessionId).count()
#             session = session.__dict__
#             session['total'] = total
#         for course in courses:
#             course_sessions = db.query(CourseSession).filter(
#                 course.course_id == CourseSession.course_id).all()
#             course_tutors = db.query(Tutor).filter(CourseTutor.course_id == course.course_id,
#                                                    Tutor.tutor_id == CourseTutor.tutor_id).first()
#             course = course.__dict__
#             course['sessions'] = course_sessions
#             course['Tutor'] = course_tutors
#             course['total'] = sessions
#             all_courses.append(course)
# --------------------------------------------------------------------------------------------
# all_courses = db.query(Course).all()
#         all_sessions = db.query(CourseSession).all()
#         for session in all_sessions:
#             total = db.query(SessionEnrolled).where(
#                 session.session_id == SessionEnrolled.sessionId).count()
#             session = session.__dict__
#             session['total'] = total
#         for course in all_courses:
#             sessions = db.query(CourseSession).filter(course.course_id == CourseSession.course_id).all()
#             course_tutor = db.query(Tutor).filter(CourseTutor.course_id == course.course_id,
#                                                   Tutor.tutor_id == CourseTutor.tutor_id).first()
#             studentName = None
#             image=None
#             if course_tutor is not None:
#                 student = db.query(Student).filter(Student.student_id == course_tutor.student_id).first()
#                 studentName = student.full_name
#                 image = db.query(StudentImages).filter(StudentImages.id == student.student_image_id).first().imagePath
#             course = course.__dict__
#             course['sessions'] = sessions
#             course['tutor_name'] = studentName
#             course['tutor_image'] = image
