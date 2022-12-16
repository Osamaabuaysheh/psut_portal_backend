from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base_class import Base


class PermitHolders(Base):
    __tablename__ = "permitHolders"
    permit_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    car_owner_name = Column(String, nullable=False)
    phone_number = Column(Integer, nullable=False)
    car_color = Column(String, nullable=False)
    car_type = Column(String, nullable=False)
    license_number = Column(String, nullable=False)
    permit_number = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False)
