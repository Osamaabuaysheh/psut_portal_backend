from typing import Any
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.Image import ImageCreateName
from app.models.Images import Images
from fastapi.responses import FileResponse

router = APIRouter()


@router.post("/events/uploadImage")
async def upload_image(
        *,
        db: Session = Depends(get_db),
        file: UploadFile = File(...),
) -> Any:
    extension = file.filename.split(".")[1]
    if extension not in ["png", "jpg", "jpeg"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="File extension not allowed")

    try:
        with open(f'static/images/Events/{file.filename}', 'wb') as f:
            while contents := file.file.read():
                f.write(contents)
                image = db.query(Images).filter(Images.name == file.filename).first()
                if not image:
                    image_in = ImageCreateName(name=file.filename, image=f'static/images/Events/{file.filename}')
                    db_in = Images(**image_in.dict())
                    db.add(db_in)
                    db.commit()
                    db.refresh(db_in)
                    return "Image Uploaded Successfully"
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}


@router.get('/get_images', response_class=FileResponse)
async def get_images(*, db: Session = Depends(get_db)):
    image = db.query(Images).filter(Images.id == 5).first()
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image Not Found")

    return image.image
