from sqlalchemy import Column, Integer, String, Time, ForeignKey

from app.db.base_class import Base


class BusRoute(Base):
    __tablename__ = "BusRoutes"
    bus_route_id = Column(Integer, primary_key=True, index=True)
    mon_wed_back = Column(Integer, nullable=True)
    mon_wed_presence = Column(Integer, nullable=True)
    sun_tue_thu_back = Column(Integer, nullable=True)
    sun_tue_thu_presence = Column(Integer, nullable=True)
    pickup_dropoff = Column(String, nullable=False)
    route = Column(String, nullable=False)
    student_id = Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False)
