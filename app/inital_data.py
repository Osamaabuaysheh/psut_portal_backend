import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:newpassword@localhost:5432/psut_portal'

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# db = SessionLocal()
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    user_role = Column(String, nullable=False)


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None
    user_role: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


def init_db(db: Session) -> None:
    user = db.query(User).filter(User.email == 'admin@psutPortal.com').first()
    if not user:
        user_in = UserCreate(
            email='admin@psutPortal.com',
            full_name="Admin User",
            password='admin',
            is_superuser=True,
            user_role="SUPERUSER"
        )
        db_obj = User(
            email=user_in.email,
            hashed_password=pwd_context.hash(user_in.password),
            full_name=user_in.full_name,
            is_superuser=user_in.is_superuser,
            user_role=user_in.user_role
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)


def init() -> None:
    db = SessionLocal()
    init_db(db)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
