from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import CourseSession, User
from app.schemas.courseSession import CreateCourseSession
from app.crud.crud_course_session import crudCourseSession
from app.api.deps import get_current_user

router = APIRouter()


@router.get('/get_All_Courses_Sessions')
async def get_course_session(*, db: Session = Depends(get_db)):
    return db.query(CourseSession.CourseSession).all()


@router.post('/Create_Course_Session')
async def create_course_session(*, db: Session = Depends(get_db), obj_in: CreateCourseSession = Depends(),
                                current_user: User.User = Depends(get_current_user)):
    return crudCourseSession.create_course_session(db=db, obj_in=obj_in)

#
# @router.post('/get_tutor_details')
# async def create_course(*, db: Session = Depends(get_db), obj_in: CreateCourse = Depends(),
#                         current_user: User.User = Depends(get_current_user)):
#     return crudCourse.create_course(db=db, obj_in=obj_in)
