from sqlalchemy import Column, Integer, String, Date, Time
from app.db.base_class import Base
from sqlalchemy.orm import relationship


class Event(Base):
    __tablename__ = "Events"
    event_id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    description = Column(String, nullable=False)
    image = Column(String, nullable=True)
    organizers = relationship("Organizer")
