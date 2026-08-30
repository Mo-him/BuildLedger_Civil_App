import uuid
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.bill import Bill
from app.models.bill_payment import BillPayment
from app.models.bill_status_history import BillStatusHistory
from app.repositories.bill_repository import (
    add_bill_payment,
    delete_bill_payment,
    get_bill_payment_by_id,
    get_bill_payments,
    update_bill_payment,
)


def _get_owned_bill(db: Session, bill_id: uuid.UUID, user_id: uuid.UUID) -> Bill:
    bill = db.scalar(select(Bill).where(Bill.id == bill_id, Bill.user_id == user_id))
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return bill


def _recalculate_payment_state(db: Session, bill: Bill, user_id: uuid.UUID) -> None:
    paid_total = db.scalar(
        select(func.coalesce(func.sum(BillPayment.payment_amount), 0))
        .where(BillPayment.bill_id == bill.id)
    ) or Decimal("0")

    old_status = bill.status
    bill.paid_amount = Decimal(paid_total)
    bill.balance_amount = max(
        bill.net_payable_amount - bill.paid_amount,
        Decimal("0"),
    )

    if bill.balance_amount == 0 and bill.net_payable_amount > 0:
        new_status = "Paid"
    elif bill.paid_amount > 0:
        new_status = "Partially Paid"
    elif old_status in {"Partially Paid", "Paid"}:
        new_status = "Approved"
    else:
        new_status = old_status

    if new_status != old_status:
        bill.status = new_status
        db.add(
            BillStatusHistory(
                id=uuid.uuid4(),
                bill_id=bill.id,
                old_status=old_status,
                new_status=new_status,
                changed_by=user_id,
                remarks="Payment state updated",
            )
        )


def add_payment(
    db: Session,
    bill_id: uuid.UUID,
    user_id: uuid.UUID,
    payment_amount: Decimal,
    payment_date,
    payment_mode: str,
    transaction_reference: str | None = None,
    remarks: str | None = None,
) -> BillPayment:
    bill = _get_owned_bill(db, bill_id, user_id)

    if bill.status not in {"Approved", "Partially Paid"}:
        raise HTTPException(
            status_code=400,
            detail="Payments can only be added to Approved or Partially Paid bills",
        )
    if payment_amount <= 0:
        raise HTTPException(status_code=400, detail="Payment amount must be greater than zero")

    remaining = max(bill.net_payable_amount - bill.paid_amount, Decimal("0"))
    if payment_amount > remaining:
        raise HTTPException(
            status_code=400,
            detail=f"Payment amount cannot exceed remaining balance of {remaining}",
        )

    payment = BillPayment(
        id=uuid.uuid4(), bill_id=bill_id, payment_amount=payment_amount,
        payment_date=payment_date, payment_mode=payment_mode,
        transaction_reference=transaction_reference, remarks=remarks,
    )
    db.add(payment)
    _recalculate_payment_state(db, bill, user_id)
    db.commit()
    db.refresh(payment)
    return payment


def get_all_payments(db: Session, bill_id: uuid.UUID, user_id: uuid.UUID) -> list[BillPayment]:
    _get_owned_bill(db, bill_id, user_id)
    return get_bill_payments(db, bill_id)


def get_payment(db: Session, bill_id: uuid.UUID, payment_id: uuid.UUID, user_id: uuid.UUID) -> BillPayment:
    _get_owned_bill(db, bill_id, user_id)
    payment = get_bill_payment_by_id(db, bill_id, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


def update_payment(db: Session, bill_id: uuid.UUID, payment_id: uuid.UUID, user_id: uuid.UUID, **data) -> BillPayment:
    bill = _get_owned_bill(db, bill_id, user_id)
    payment = get_payment(db, bill_id, payment_id, user_id)

    old_amount = payment.payment_amount
    new_amount = data.get("payment_amount", old_amount)
    if new_amount <= 0:
        raise HTTPException(status_code=400, detail="Payment amount must be greater than zero")

    current_paid_excluding = bill.paid_amount - old_amount
    if current_paid_excluding + new_amount > bill.net_payable_amount:
        raise HTTPException(status_code=400, detail="Payment amount exceeds bill balance")

    for field, value in data.items():
        if value is not None:
            setattr(payment, field, value)

    _recalculate_payment_state(db, bill, user_id)
    db.commit()
    db.refresh(payment)
    return payment


def remove_payment(db: Session, bill_id: uuid.UUID, payment_id: uuid.UUID, user_id: uuid.UUID) -> None:
    bill = _get_owned_bill(db, bill_id, user_id)
    payment = get_payment(db, bill_id, payment_id, user_id)
    db.delete(payment)
    db.flush()
    _recalculate_payment_state(db, bill, user_id)
    db.commit()
