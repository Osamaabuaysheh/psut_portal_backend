from typing import Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.CourseRequests import CourseRequests
from app.schemas.CourseRequests import CreateCourseRequest, UpdateCourseRequest


class CRUDCourseRequets(CRUDBase[CourseRequests, CreateCourseRequest, UpdateCourseRequest]):
    def get_by_id(self, db: Session, *, course_request_id: int) -> Optional[CourseRequests]:
        return db.query(self.model).filter(CourseRequests.request_id == course_request_id).first()

    def delete_course_request(self, db: Session, *, course_request_id: int):
        db_obj = db.query(self.model).filter(CourseRequests.request_id == course_request_id).delete()
        db.commit()
        return db_obj

    def create_course_request(self, db: Session, *, obj_in: CreateCourseRequest):
        course_req_obj = CourseRequests(
            course_id=obj_in.course_id,
            student_id=obj_in.student_id
        )
        db.add(course_req_obj)
        db.commit()
        db.refresh(course_req_obj)

        return course_req_obj


crudCourseRequests = CRUDCourseRequets(CourseRequests)
