from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.crud.crud_organizer import crudOrganizer
from app.db.database import get_db
from app.models import Organizers, User
from app.schemas.organizer import OrganizerCreate

router = APIRouter()


@router.get('/get_All_Organizers')
async def get_all_organizers(*, db: Session = Depends(get_db), current_user: User.User = Depends(get_current_user)):
    return db.query(Organizers.Organizer).all()


@router.post('/create_Organizer')
async def get_all_organizers(*, db: Session = Depends(get_db), org_in: OrganizerCreate = Depends(),
                             org_image: UploadFile = File(...), current_user: User.User = Depends(get_current_user)):
    extension = org_image.filename.split(".")[1]
    if extension not in ["png", "jpg", "jpeg", "gif"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="File extension not allowed")
    return crudOrganizer.create_organizer(db=db, obj_in=org_in, image_name=org_image.filename)
