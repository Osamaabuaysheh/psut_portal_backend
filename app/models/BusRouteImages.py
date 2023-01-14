from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class BusRouteImages(Base):
    __tablename__ = "busRouteImages"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    image = Column(String, nullable=False)
    ramadan_image = Column(String, nullable=True)
