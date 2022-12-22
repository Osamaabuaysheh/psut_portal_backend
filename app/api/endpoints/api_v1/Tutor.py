from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.crud.crud_tutor import crudTutor
from app.db.database import get_db
from app.models import Tutor, User
from app.schemas.Tutor import TutorCreate

router = APIRouter()


@router.get('/get_All_Tutors')
async def get_tutors(*, db: Session = Depends(get_db)):
    return db.query(Tutor.Tutor).all()


@router.post('/Create_Tutor')
async def create_tutor(*, db: Session = Depends(get_db), obj_in: TutorCreate = Depends(),
                       current_user: User.User = Depends(get_current_user)):
    return crudTutor.create_tutor(db=db, obj_in=obj_in, owner=current_user.id)
