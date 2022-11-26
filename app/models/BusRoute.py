from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base_class import Base


class BusRoute(Base):
    __tablename__ = "BusRoutes"
    bus_route_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    bus_route_name = Column(String, nullable=False)
    first_route = Column(String, nullable=False)
    second_route = Column(String, nullable=False)
    third_route = Column(String, nullable=False)
    fourth_route = Column(String, nullable=True)
    location_trip = Column(String, nullable=False)
