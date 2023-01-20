from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_current_active_superuser
from app.core.security import verify_password, get_password_hash
from app.crud.crud_user import crud_user
from app.db.database import get_db
from app.models.User import User
from app.schemas.User import UserCreate, UserUpdate

router = APIRouter()


@router.get("/users")
def get_users(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: User = Depends(get_current_user)
) -> Any:
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.post("/create_user")
def create_user(
        *,
        db: Session = Depends(get_db),
        user_in: UserCreate,
        current_user: User = Depends(get_current_active_superuser),
) -> Any:
    user = crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(  # handling errors, exception with additional data relevant for APIs.
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud_user.create(db, obj_in=user_in)
    return user


@router.post("/login_admin_data")
def login_admin(
        *,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
) -> Any:
    return current_user


@router.post("/delete_admin/{admin_id}")
def delete_admin(
        *, db: Session = Depends(get_db), current_user: User = Depends(get_current_user), admin_id: int
) -> Any:
    admin = db.query(User).filter(User.id == admin_id).first()
    if admin is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Admin Doesn't Exist")
    crud_user.delete_admin(db=db, admin_id=admin_id)

    raise HTTPException(status_code=status.HTTP_200_OK, detail="Admin Deleted")


@router.post("/reset-password-admin/{admin_id}")
def delete_admin(
        *, db: Session = Depends(get_db), current_user: User = Depends(get_current_user), admin_id: int
) -> Any:
    admin = db.query(User).filter(User.id == admin_id).first()
    if admin is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Admin Doesn't Exist")
    crud_user.delete_admin(db=db, admin_id=admin_id)

    raise HTTPException(status_code=status.HTTP_200_OK, detail="Admin Deleted")


@router.post("/forget-password/{user_id}")
def update_user(
        *,
        db: Session = Depends(get_db),
        user_id: int,
        user_in: UserUpdate,
        current_user: User = Depends(get_current_user),
) -> Any:
    """
    Update a user.
    """
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    check = verify_password(user_in.password, hashed_password=user.hashed_password)
    if check:
        user = crud_user.update(db, db_obj=user, obj_in=user_in)
        return user
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='password Not Correct')


@router.post("/update_admin/{admin_id}")
def update_admin(
        *, db: Session = Depends(get_db), current_user: User = Depends(get_current_user), admin_id: int,
        obj_in: UserUpdate
) -> Any:
    if obj_in.password is None:
        db.query(User).filter(User.id == admin_id).update(values=obj_in.dict(exclude_none=True))
        db.commit()
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Admin Updated Successfully")
    else:
        update_data = obj_in.dict(exclude_unset=True)
        hashed_password = get_password_hash(obj_in.password)
        del update_data["password"]
        update_data["hashed_password"] = hashed_password
        db.query(User).filter(User.id == admin_id).update(values=update_data)
        db.commit()
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Admin Updated Successfully")
