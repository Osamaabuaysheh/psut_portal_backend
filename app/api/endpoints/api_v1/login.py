from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud
from app.core import security
from app.core.config import settings
from app.db.database import get_db
from app.models.User import User
from app.schemas import token
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/")
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    # current_user: models.User = Depends(deps.get_current_active_superuser),#depends:has the same shape and structure that all your path operation functions have.
) -> Any:
    """
    Retrieve users.
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.post("/login/access-token", response_model=token.Token, status_code=status.HTTP_200_OK)
def login_access_token(
        db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = db.query(User).filter(
        User.email == form_data.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials PASSWORD")

    # create a token
    # return token

    access_token = security.create_access_token(user.id,
                                                expires_delta=timedelta(minutes=settings.access_token_expire_minutes))

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/reset-password/")
def reset_password(current_user=Depends(get_current_user)
):
    """
    Reset password
    """
    return current_user
