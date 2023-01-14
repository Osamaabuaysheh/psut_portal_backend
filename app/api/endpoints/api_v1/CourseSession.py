from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.crud.crud_course_session import crudCourseSession
from app.db.database import get_db
from app.models import CourseSession, User, SessionEnrolled
from app.schemas.courseSession import CreateCourseSession, UpdateCourseSession

router = APIRouter()


@router.get('/get_all_courses_sessions_details')
async def get_course_details(*, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crudCourseSession.get_course_session_details(db=db)


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


@router.post('/delete_course_session/{course_session_id}')
async def create_course_session(*, db: Session = Depends(get_db), course_session_id: int,
                                current_user: User.User = Depends(get_current_user)):
    course_session = db.query(CourseSession.CourseSession).filter(
        CourseSession.CourseSession.session_id == course_session_id)
    if course_session.first() is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Session Doesn't Exist")
    else:
        crudCourseSession.delete_session(db=db, course_session_id=course_session_id)
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Session Deleted Successfully")


@router.post('/update_course_details/')
async def update_course_session(*, db: Session = Depends(get_db), course_id: int,
                                obj_in: UpdateCourseSession = Depends(),
                                current_user: User.User = Depends(get_current_user)):
    all_sessions = db.query(CourseSession.CourseSession).filter(
        CourseSession.CourseSession.course_id == course_id).all()
    if not all_sessions:
        obj = CourseSession.CourseSession(course_id=course_id, tutor_id=obj_in.tutor_id)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Created Course Successfully")
    for index, session in enumerate(all_sessions):
        if not obj_in.sessions:
            db.query(CourseSession.CourseSession).filter(CourseSession.CourseSession.course_id == course_id).update(
                values={'tutor_id': obj_in.tutor_id})
            db.commit()
            raise HTTPException(status_code=status.HTTP_200_OK, detail="Updated Successfully HERE")
        db.query(CourseSession.CourseSession).filter(course_id == session.course_id and obj_in.sessions[
            index].session_id == CourseSession.CourseSession.session_id).update(
            values={'start_time': obj_in.sessions[index].start_time, 'end_time': obj_in.sessions[index].end_time,
                    'day': obj_in.sessions[index].day, 'tutor_id': obj_in.tutor_id})
        db.commit()
    raise HTTPException(status_code=status.HTTP_200_OK, detail="Updated Successfully")
