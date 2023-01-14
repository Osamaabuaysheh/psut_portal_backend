from typing import Optional

import pandas as pd
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.crud.crud_student import crudStudent
from app.models.PermitHolders import PermitHolders
from app.models.Student import Student
from app.schemas.permitHolders import PermitHolderCreate, PermitHolderUpdate


class CRUDPermitHolders(CRUDBase[PermitHolders, PermitHolderCreate, PermitHolderUpdate]):
    def get_by_id(self, db: Session, *, permit_id: int) -> Optional[PermitHolders]:
        return db.query(self.model).filter(PermitHolders.permit_id == permit_id).first()

    def get_by_student_id(self, db: Session, *, student_id: int):
        permit_details = db.query(self.model).filter(PermitHolders.student_id == student_id).first()
        student = db.query(Student).filter(Student.student_id == permit_details.student_id).first()
        if student is None:
            return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Student not found")

        return {'colleage': student.colleage, 'permit_number': permit_details.permit_number}

    def get_by_permit_id(self, db: Session, *, permit_id: int) -> Optional[PermitHolders]:
        return db.query(self.model).filter(PermitHolders.permit_number == permit_id).first()

    def add_all_permit_holders(self, db: Session, *, file, current_user: int):

        csv_reader = pd.read_excel(
            f"static/Permits/{file.filename}", skiprows=[0])
        csv_reader.rename(columns={'لون السيارة ': 'لون السيارة'}, inplace=True)
        csv_reader = csv_reader[csv_reader['رقم الهاتف'].notna()]
        csv_reader['رقم الهاتف'] = csv_reader['رقم الهاتف'].astype(int)
        first = csv_reader.to_numpy()
        all_data = []
        for row in range(len(first)):
            data = {}
            for col in range(0, 7):
                data['Phone'] = first[row][1]
                data['color'] = first[row][2]
                data['license_number'] = str(first[row][3])
                data['Car_Type'] = first[row][4]
                data['StudentID'] = first[row][5]
                data['name'] = first[row][6]
            all_data.append(data)

        for index, data in enumerate(all_data):
            try:
                std = crudStudent.get_by_id(db=db, student_id=data['StudentID'])
                if std is None:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student Doesn't Exist")
                permit = db.query(PermitHolders).filter(data['StudentID'] == PermitHolders.student_id).first()
                if permit is not None:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Permit Already Exists")
                db_obj = PermitHolders(
                    student_id=data['StudentID'],
                    permit_number=index + 1,
                    car_owner_name=data['name'],
                    car_type=data['Car_Type'],
                    car_color=data['color'],
                    phone_number=data['Phone'],
                    license_number=data['license_number'],
                    owner_id=current_user
                )
                db.add(db_obj)
                db.commit()
                db.refresh(db_obj)
            except:
                continue

        raise HTTPException(status_code=status.HTTP_200_OK, detail="Data Stored")


def delete_event_by_id(self, db: Session, *, permit_id: int):
    permit = db.query(self.model).filter(PermitHolders.permit_id == permit_id)
    if permit.first() is None:
        return permit
    else:
        permit.delete()
        db.commit()
        return "Event Deleted"


def create_permit_holder(self, db: Session, *, obj_in: PermitHolderCreate, current_user: int):
    db_obj = PermitHolders(
        student_id=obj_in.student_id,
        permit_number=obj_in.permit_number,
        car_owner_name=obj_in.car_owner_name,
        car_type=obj_in.car_type,
        car_color=obj_in.car_color,
        phone_number=obj_in.phone_number,
        license_number=obj_in.license_number,
        owner_id=current_user
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)

    return db_obj


crudPermitHolders = CRUDPermitHolders(PermitHolders)
