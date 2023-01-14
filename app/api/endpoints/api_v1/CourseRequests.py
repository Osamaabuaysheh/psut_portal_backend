from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_current_student
from app.crud.crud_course_requests import crudCourseRequests
from app.db.database import get_db
from app.models import User
from app.models.Course import Course
from app.models.CourseRequests import CourseRequests
from app.models.CourseSession import CourseSession
from app.models.Student import Student
from app.models.course_tutor import CourseTutor
from app.schemas.CourseRequests import CreateCourseRequest

router = APIRouter()


@router.get('/get_All_Course_Requests')
async def get_courses(*, db: Session = Depends(get_db), current_user: User.User = Depends(get_current_user)):
    courses = db.query(CourseRequests.course_id, func.count(CourseRequests.course_id).label('count')).group_by(
        CourseRequests.course_id).all()
    total_courses = []
    for course in courses:
        course_dict = {
            "Course_id": course.course_id,
            "Total": course.count,
            "Course_Name": db.query(Course).filter(Course.course_id == course.course_id).first().course_name}
        total_courses.append(course_dict)
    return total_courses


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
    student = db.query(CourseRequests.student_id == obj_in.student_id).first()
    if student is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Request With This student id already exists")
    if course is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Course Doesn't Exist")
    crudCourseRequests.create_course_request(db=db, obj_in=obj_in)
    raise HTTPException(status_code=status.HTTP_200_OK, detail="Course Request Created")


@router.post('/delete_course_request/{course_id}')
async def get_courses(*, db: Session = Depends(get_db), current_user: User.User = Depends(get_current_user),
                      course_id: int):
    course_request = db.query(CourseRequests).filter(CourseRequests.course_id == course_id).all()
    if course_request is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Course Requset Doesn't Exist")
    for course in course_request:
        db.query(CourseRequests).filter(CourseRequests.course_id == course.course_id).delete()
        db.commit()
    raise HTTPException(status_code=status.HTTP_200_OK, detail="Course Request Deleted")


@router.get('/get_All_Courses_Tutors')
async def get_courses(*, db: Session = Depends(get_db), current_user: User.User = Depends(get_current_user),
                      course_id: int, student_id: int):
    return db.query(CourseTutor).all()


@router.post('/accept_course_request/{request_id}')
async def get_courses(*, db: Session = Depends(get_db), current_user: User.User = Depends(get_current_user),
                      course_id: int, tutor_id: int, request_id: int):
    course_obj = CourseSession(course_id=course_id, tutor_id=tutor_id)
    db.add(course_obj)
    db.commit()
    db.refresh(course_obj)
    course_request = db.query(CourseRequests).filter(CourseRequests.course_id == course_id).all()
    if course_request is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Course Requset Doesn't Exist")
    for course in course_request:
        db.query(CourseRequests).filter(CourseRequests.course_id == course.course_id).delete()
        db.commit()
    raise HTTPException(status_code=status.HTTP_200_OK, detail="Course Accepted")
