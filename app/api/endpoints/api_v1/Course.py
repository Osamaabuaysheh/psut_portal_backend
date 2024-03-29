from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_current_student
from app.crud.crud_course import crudCourse
from app.db.database import get_db
from app.models import Course, User
from app.models.CourseRequests import CourseRequests
from app.models.Student import Student
from app.models.Tutor import Tutor
from app.models.TutorRequests import TutorRequests
from app.schemas.Course import CreateCourse

router = APIRouter()


@router.get('/get_All_Courses')
async def get_courses(*, db: Session = Depends(get_db)):
    return db.query(Course.Course).all()


@router.get('/get_All_Courses_Tutors')
async def get_course_details(*, db: Session = Depends(get_db), current_user: User.User = Depends(get_current_user)):
    return {'courses': db.query(Course.Course).all(), 'tutors': db.query(Tutor).all(),
            'Tutor_Requests': db.query(TutorRequests).all(), 'Course_Requests': db.query(CourseRequests).all()}


@router.get('/get_course_details')
async def get_course_details(*, db: Session = Depends(get_db), current_user: Student = Depends(get_current_student)):
    return crudCourse.get_course_details(db=db)


@router.post('/Create_Course')
async def create_course(*, db: Session = Depends(get_db), obj_in: CreateCourse = Depends(),
                        current_user: User.User = Depends(get_current_user)):
    return crudCourse.create_course(db=db, obj_in=obj_in)
