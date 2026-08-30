import uuid
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.bill import Bill
from app.models.bill_previous_payment import BillPreviousPayment
from app.repositories.bill_repository import (
    add_previous_payment,
    delete_previous_payment,
    get_previous_payment_by_id,
    get_previous_payments,
    update_previous_payment,
)


def _get_owned_bill(db: Session, bill_id: uuid.UUID, user_id: uuid.UUID) -> Bill:
    bill = db.scalar(select(Bill).where(Bill.id == bill_id, Bill.user_id == user_id))
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return bill


def get_all_previous_payments(db: Session, bill_id: uuid.UUID, user_id: uuid.UUID) -> list[BillPreviousPayment]:
    _get_owned_bill(db, bill_id, user_id)
    return get_previous_payments(db, bill_id)


def get_previous_payment(db: Session, bill_id: uuid.UUID, previous_payment_id: uuid.UUID, user_id: uuid.UUID) -> BillPreviousPayment:
    _get_owned_bill(db, bill_id, user_id)
    payment = get_previous_payment_by_id(db, bill_id, previous_payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Previous payment not found")
    return payment


def create_previous_payment(db: Session, bill_id: uuid.UUID, user_id: uuid.UUID, previous_bill_amount: Decimal, previous_payment_amount: Decimal, balance_carried_forward: Decimal, payment_date, reference_number: str | None = None, remarks: str | None = None) -> BillPreviousPayment:
    bill = _get_owned_bill(db, bill_id, user_id)
    if bill.status not in {"Draft", "Rejected"}:
        raise HTTPException(status_code=400, detail="Previous payments can only be changed on Draft or Rejected bills")
    if any(v < 0 for v in (previous_bill_amount, previous_payment_amount, balance_carried_forward)):
        raise HTTPException(status_code=400, detail="Previous payment values cannot be negative")

    payment = BillPreviousPayment(
        id=uuid.uuid4(), bill_id=bill_id,
        previous_bill_amount=previous_bill_amount,
        previous_payment_amount=previous_payment_amount,
        balance_carried_forward=balance_carried_forward,
        payment_date=payment_date,
        reference_number=reference_number,
        remarks=remarks,
    )
    saved = add_previous_payment(db, payment)
    from app.services.bill_calculation_service import recalculate_bill_totals
    recalculate_bill_totals(db, bill_id)
    return saved


def update_previous_payment_details(db: Session, bill_id: uuid.UUID, previous_payment_id: uuid.UUID, user_id: uuid.UUID, **data) -> BillPreviousPayment:
    bill = _get_owned_bill(db, bill_id, user_id)
    if bill.status not in {"Draft", "Rejected"}:
        raise HTTPException(status_code=400, detail="Previous payments can only be changed on Draft or Rejected bills")
    payment = get_previous_payment(db, bill_id, previous_payment_id, user_id)
    for field, value in data.items():
        if value is not None:
            setattr(payment, field, value)
    saved = update_previous_payment(db, payment)
    from app.services.bill_calculation_service import recalculate_bill_totals
    recalculate_bill_totals(db, bill_id)
    return saved


def remove_previous_payment(db: Session, bill_id: uuid.UUID, previous_payment_id: uuid.UUID, user_id: uuid.UUID) -> None:
    bill = _get_owned_bill(db, bill_id, user_id)
    if bill.status not in {"Draft", "Rejected"}:
        raise HTTPException(status_code=400, detail="Previous payments can only be changed on Draft or Rejected bills")
    payment = get_previous_payment(db, bill_id, previous_payment_id, user_id)
    delete_previous_payment(db, payment)
    from app.services.bill_calculation_service import recalculate_bill_totals
    recalculate_bill_totals(db, bill_id)
