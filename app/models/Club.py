from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base_class import Base


class Club(Base):
    __tablename__ = "Clubs"
    club_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    club_name = Column(String, primary_key=True)
    club_image = Column(String, nullable=False)
    club_icon_image = Column(String, nullable=False)
    description = Column(String, nullable=False)
    link = Column(String, nullable=False)
    contact_info = Column(String, nullable=False)
