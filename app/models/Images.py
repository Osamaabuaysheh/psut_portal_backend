from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class Images(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    image = Column(String, nullable=False)
