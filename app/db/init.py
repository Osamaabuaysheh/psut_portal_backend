from sqlalchemy.orm import Session

from app.schemas.User import UserCreate
from app.core.config import settings
from app.db import base  # noqa: F401
from app.models.User import User
from app.core.security import get_password_hash


def init_db(db: Session) -> None:
    user = db.query(User).filter(User.email == settings.FIRST_SUPERUSER).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        db_obj = User(
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password),
            full_name=user_in.full_name,
            is_superuser=user_in.is_superuser,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
