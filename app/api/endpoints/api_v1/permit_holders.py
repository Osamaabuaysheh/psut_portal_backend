from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.crud.crud_permit_holder import crudPermitHolders
from app.db.database import get_db
from app.models.User import User
from app.schemas.permitHolders import PermitHolderCreate

router = APIRouter()


@router.get('/get_all_permit_numbers')
async def get_permit_numbers(*, db: Session = Depends(get_db)):
    return crudPermitHolders.get_multi(db=db)


@router.post('/create_permit_holder')
async def create_permit_holder(*, db: Session = Depends(get_db), obj_in: PermitHolderCreate = Depends(),
                               current_user: User = Depends(get_current_user)):
    return crudPermitHolders.create_permit_holder(db=db, obj_in=obj_in, current_user=current_user.id)


@router.get('/get_permit_by_student_id/{student_id}')
async def get_permit_holder_by_student_id(*, db: Session = Depends(get_db), student_id: int):
    return crudPermitHolders.get_by_student_id(db=db, student_id=student_id)


@router.get('/ger_permit_by_permit_id/{permit_id}')
async def get_permit_holder_by_permit_id(*, db: Session = Depends(get_db), permit_id: int):
    return crudPermitHolders.get_by_permit_id(db=db, permit_id=permit_id)


@router.post('/upload_permit_holders')
async def upload_permit_holder(*, db: Session = Depends(get_db), file: UploadFile = File(...),
                               current_user: User = Depends(get_current_user)):
    extension = file.filename.split(".")[1]
    if extension not in ["xlsx"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="File extension not allowed")
    try:
        with open(f"static/Permits/{file.filename}", 'wb') as f:
            while contents := file.file.read():
                f.write(contents)
        db = crudPermitHolders.add_all_permit_holders(db=db, file=file, current_user=current_user.id)

        return db

    finally:
        file.file.close()
