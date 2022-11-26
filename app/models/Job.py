from sqlalchemy import Column, Integer, String, Date
from app.db.base_class import Base


class Job(Base):
    __tablename__ = "Jobs"
    job_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    job_title = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    college = Column(String, nullable=False)
    job_responsanbilities = Column(String, nullable=False)
    job_requierments = Column(String, nullable=False)
    job_Deadline = Column(Date, nullable=False)
    job_icon_image = Column(String, nullable=False)
    job_description = Column(String, nullable=False)
