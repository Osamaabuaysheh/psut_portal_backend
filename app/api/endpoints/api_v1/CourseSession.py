from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.crud.crud_course_session import crudCourseSession
from app.db.database import get_db
from app.models import CourseSession, User, SessionEnrolled
from app.schemas.courseSession import CreateCourseSession

router = APIRouter()


@router.get('/get_All_Courses_Sessions')
async def get_course_session(*, db: Session = Depends(get_db)):
    sessions = db.query(CourseSession.CourseSession).all()
    for session in sessions:
        total = db.query(SessionEnrolled.SessionEnrolled).where(
            session.session_id == SessionEnrolled.SessionEnrolled.sessionId).count()
        session = session.__dict__
        session['total'] = total

    return sessions


@router.post('/Create_Course_Session')
async def create_course_session(*, db: Session = Depends(get_db), obj_in: CreateCourseSession = Depends(),
                                current_user: User.User = Depends(get_current_user)):
    return crudCourseSession.create_course_session(db=db, obj_in=obj_in)


@router.delete('/delete_course_session/{course_session_id}')
async def create_course_session(*, db: Session = Depends(get_db), course_session_id: int,
                                current_user: User.User = Depends(get_current_user)):
    course_session = db.query(CourseSession.CourseSession).filter(
        CourseSession.CourseSession.session_id == course_session_id)
    if course_session.first() is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Session Doesn't Exist")
    else:
        crudCourseSession.delete_session(db=db, course_session_id=course_session_id)
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Session Deleted Successfully")
