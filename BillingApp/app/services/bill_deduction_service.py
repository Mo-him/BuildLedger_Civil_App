import uuid
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.bill import Bill
from app.models.bill_deduction import BillDeduction
from app.repositories.bill_repository import (
    add_bill_deduction,
    delete_bill_deduction,
    get_bill_deduction_by_id,
    get_bill_deductions,
    update_bill_deduction,
)


def _get_owned_bill(db: Session, bill_id: uuid.UUID, user_id: uuid.UUID) -> Bill:
    bill = db.scalar(select(Bill).where(Bill.id == bill_id, Bill.user_id == user_id))
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return bill


def get_all_bill_deductions(db: Session, bill_id: uuid.UUID, user_id: uuid.UUID) -> list[BillDeduction]:
    _get_owned_bill(db, bill_id, user_id)
    return get_bill_deductions(db, bill_id)


def get_bill_deduction(db: Session, bill_id: uuid.UUID, deduction_id: uuid.UUID, user_id: uuid.UUID) -> BillDeduction:
    _get_owned_bill(db, bill_id, user_id)
    deduction = get_bill_deduction_by_id(db, bill_id, deduction_id)
    if not deduction:
        raise HTTPException(status_code=404, detail="Bill deduction not found")
    return deduction


def create_bill_deduction(db: Session, bill_id: uuid.UUID, user_id: uuid.UUID, deduction_type_id: int, percentage: Decimal | None, amount: Decimal, remarks: str | None = None) -> BillDeduction:
    bill = _get_owned_bill(db, bill_id, user_id)
    if bill.status not in {"Draft", "Rejected"}:
        raise HTTPException(status_code=400, detail="Deductions can only be changed on Draft or Rejected bills")
    if amount < 0 or (percentage is not None and not 0 <= percentage <= 100):
        raise HTTPException(status_code=400, detail="Invalid deduction amount or percentage")

    deduction = BillDeduction(
        id=uuid.uuid4(), bill_id=bill_id, deduction_type_id=deduction_type_id,
        percentage=percentage, amount=amount, remarks=remarks,
    )
    saved = add_bill_deduction(db, deduction)
    from app.services.bill_calculation_service import recalculate_bill_totals
    recalculate_bill_totals(db, bill_id)
    return saved


def update_bill_deduction_details(db: Session, bill_id: uuid.UUID, deduction_id: uuid.UUID, user_id: uuid.UUID, **data) -> BillDeduction:
    bill = _get_owned_bill(db, bill_id, user_id)
    if bill.status not in {"Draft", "Rejected"}:
        raise HTTPException(status_code=400, detail="Deductions can only be changed on Draft or Rejected bills")
    deduction = get_bill_deduction(db, bill_id, deduction_id, user_id)
    if data.get("percentage") is not None and not 0 <= data["percentage"] <= 100:
        raise HTTPException(status_code=400, detail="Deduction percentage must be between 0 and 100")
    if data.get("amount") is not None and data["amount"] < 0:
        raise HTTPException(status_code=400, detail="Deduction amount cannot be negative")
    for field, value in data.items():
        if value is not None:
            setattr(deduction, field, value)
    saved = update_bill_deduction(db, deduction)
    from app.services.bill_calculation_service import recalculate_bill_totals
    recalculate_bill_totals(db, bill_id)
    return saved


def remove_bill_deduction(db: Session, bill_id: uuid.UUID, deduction_id: uuid.UUID, user_id: uuid.UUID) -> None:
    bill = _get_owned_bill(db, bill_id, user_id)
    if bill.status not in {"Draft", "Rejected"}:
        raise HTTPException(status_code=400, detail="Deductions can only be changed on Draft or Rejected bills")
    deduction = get_bill_deduction(db, bill_id, deduction_id, user_id)
    delete_bill_deduction(db, deduction)
    from app.services.bill_calculation_service import recalculate_bill_totals
    recalculate_bill_totals(db, bill_id)
