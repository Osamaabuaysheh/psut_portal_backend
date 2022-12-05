from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import Course, User, CourseSession
from app.schemas.Course import CreateCourse
from app.crud.crud_course import crudCourse
from app.api.deps import get_current_user

router = APIRouter()


@router.get('/get_All_Courses')
async def get_courses(*, db: Session = Depends(get_db)):
    return db.query(Course.Course).all()


@router.post('/Create_Course')
async def create_course(*, db: Session = Depends(get_db), obj_in: CreateCourse = Depends(),
                        current_user: User.User = Depends(get_current_user)):
    return crudCourse.create_course(db=db, obj_in=obj_in)


@router.get('/get_course_details')
async def get_course_details(*, db: Session = Depends(get_db)):
    return crudCourse.get_course_details(db=db)
