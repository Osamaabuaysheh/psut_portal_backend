from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.User import User
from app.schemas.User import UserCreate
from app.api.deps import get_current_user, get_current_active_superuser
from app.crud.crud_user import crud_user
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.get("/users")
def get_users(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: User = Depends(get_current_user)
) -> Any:
    print(current_user)
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
