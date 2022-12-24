from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_current_student
from app.crud.crud_course_requests import crudCourseRequests
from app.db.database import get_db
from app.models import User
from app.models.Course import Course
from app.models.CourseRequests import CourseRequests
from app.models.Student import Student
from app.schemas.CourseRequests import CreateCourseRequest

router = APIRouter()


@router.get('/get_All_Course_Requests')
async def get_courses(*, db: Session = Depends(get_db), current_user: User.User = Depends(get_current_user)):
    return db.query(CourseRequests).all()


@router.post('/create_course_request')
async def get_courses(*, db: Session = Depends(get_db), current_user: User.User = Depends(get_current_user),
                      obj_in: CreateCourseRequest = Depends()):
    course = db.query(Course).filter(Course.course_id == obj_in.course_id).first()
    if course is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Course Doesn't Exist")
    crudCourseRequests.create_course_request(db=db, obj_in=obj_in)
    raise HTTPException(status_code=status.HTTP_200_OK, detail="Course Request Created")


@router.post('/create_course_request_student')
async def get_courses(*, db: Session = Depends(get_db), current_user: Student = Depends(get_current_student),
                      obj_in: CreateCourseRequest = Depends()):
    course = db.query(Course).filter(Course.course_id == obj_in.course_id).first()
    if course is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Course Doesn't Exist")
    crudCourseRequests.create_course_request(db=db, obj_in=obj_in)
    raise HTTPException(status_code=status.HTTP_200_OK, detail="Course Request Created")
