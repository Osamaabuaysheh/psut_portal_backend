from fastapi import APIRouter, Depends, HTTPException, Body
from typing import Any, List
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.StudentSchema import StudentSchema, StudentOut, StudentIn
from app.models.Student import Student
from app.core.security import get_password_hash

router = APIRouter()


@router.get('/get_students', response_model=List[StudentOut], response_model_exclude={'hashed_password'})
def get_students(db: Session = Depends(get_db)):
    users = db.query(Student).all()
    return users


@router.get('/get_studentsbyID', response_model=List[StudentOut], response_model_exclude={'hashed_password'})
def get_students(db: Session = Depends(get_db), student_in=StudentIn):
    users = db.query(Student).filter(Student.id == student_in.).first()
    return users


@router.post("/create_Student")
def create_user(
        *,
        db: Session = Depends(get_db),
        user_in: StudentSchema
) -> Any:
    """
    Create new user.
    """
    user = db.query(Student).filter(Student.email == user_in.email).first()
    if user:
        raise HTTPException(  # handling errors, exception with additional data relevant for APIs.
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    db_obj = Student(
        id=user_in.id,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.hashed_password),
        full_name=user_in.full_name,
        colleage=user_in.colleage
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)

    return db_obj
