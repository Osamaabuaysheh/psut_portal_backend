import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_current_student
from app.db.database import get_db
from app.models.CallLogsStudent import CallLogsStudent
from app.models.PermitHolders import PermitHolders
from app.models.Student import Student
from app.models.User import User

router = APIRouter()


@router.get('/get_all_call_logs')
async def get_all_call_logs(*, db: Session = Depends(get_db),
                            current_user: User = Depends(get_current_user)):
    return db.query(CallLogsStudent).all()


@router.post('/establish_call')
async def establish_call(*, db: Session = Depends(get_db),
                         current_user: Student = Depends(get_current_student), caller: int, receiver: int):
    receiver_std_num = db.query(PermitHolders).filter(PermitHolders.permit_number == receiver).first()
    call_obj = CallLogsStudent(caller=caller, receiver=receiver_std_num.student_id, datetime=datetime.datetime.now())
    db.add(call_obj)
    db.commit()
    db.refresh(call_obj)
    return call_obj
