from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import TutorRequests, User
from app.schemas.TutorRequest import TutorRequestCreate
from app.crud.crud_TutorRequest import crudTutorRequest
from app.api.deps import get_current_user

router = APIRouter()


@router.get('/get_All_Requests')
async def get_Requests(*, db: Session = Depends(get_db)):
    return db.query(TutorRequests.TutorRequests).all()


@router.post('/Create_Request')
async def create_request(*, db: Session = Depends(get_db), obj_in: TutorRequestCreate = Depends()):
    return crudTutorRequest.create_request(db=db, obj_in=obj_in)
