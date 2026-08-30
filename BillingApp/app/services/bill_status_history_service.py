import uuid

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.bill import Bill
from app.models.bill_status_history import BillStatusHistory
from app.repositories.bill_repository import get_status_history


def get_bill_status_history(db: Session, bill_id: uuid.UUID, user_id: uuid.UUID) -> list[BillStatusHistory]:
    bill = db.scalar(select(Bill).where(Bill.id == bill_id, Bill.user_id == user_id))
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return get_status_history(db, bill_id)
