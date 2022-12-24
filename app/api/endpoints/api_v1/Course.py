from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_current_student
from app.crud.crud_course import crudCourse
from app.db.database import get_db
from app.models import Course, User
from app.models.Student import Student
from app.schemas.Course import CreateCourse

router = APIRouter()


@router.get('/get_All_Courses')
async def get_courses(*, db: Session = Depends(get_db)):
    return db.query(Course.Course).all()


@router.get('/get_course_details')
async def get_course_details(*, db: Session = Depends(get_db), current_user: Student = Depends(get_current_student)):
    return crudCourse.get_course_details(db=db)


@router.post('/Create_Course')
async def create_course(*, db: Session = Depends(get_db), obj_in: CreateCourse = Depends(),
                        current_user: User.User = Depends(get_current_user)):
    return crudCourse.create_course(db=db, obj_in=obj_in)


@router.delete('/delet_course/{course_id}')
async def create_course(*, db: Session = Depends(get_db), course_id: int,
                        current_user: User.User = Depends(get_current_user)):
    course = db.query(Course.Course).filter(Course.Course.course_id == course_id)
    if course.first() is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Course Doesn't Exist")
    else:
        crudCourse.delete_course(db=db, course_id=course_id)
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Course Deleted Successfully")
