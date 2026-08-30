import uuid
from decimal import Decimal, ROUND_HALF_UP

from fastapi import HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.bill import Bill
from app.models.bill_calculation import BillCalculation
from app.models.bill_deduction import BillDeduction
from app.models.bill_item import BillItem
from app.models.bill_previous_payment import BillPreviousPayment
from app.models.bill_tax import BillTax
from app.repositories.bill_repository import add_bill_calculation, get_bill_calculation

MONEY = Decimal("0.01")


def _money(value: Decimal) -> Decimal:
    return Decimal(value or 0).quantize(MONEY, rounding=ROUND_HALF_UP)


def calculate_bill(
    total_items_amount: Decimal,
    other_charges: Decimal,
    total_deductions: Decimal,
    total_tax: Decimal,
    previous_amount: Decimal = Decimal("0"),
) -> dict:
    total_items_amount = _money(total_items_amount)
    other_charges = _money(other_charges)
    total_deductions = _money(total_deductions)
    total_tax = _money(total_tax)
    previous_amount = _money(previous_amount)

    gross_amount = _money(total_items_amount + other_charges)
    current_amount = _money(gross_amount - total_deductions)
    if current_amount < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Deductions cannot exceed gross amount",
        )

    net_payable = _money(current_amount + total_tax + previous_amount)

    return {
        "total_items_amount": total_items_amount,
        "other_charges": other_charges,
        "gross_amount": gross_amount,
        "total_deductions": total_deductions,
        "total_tax": total_tax,
        "previous_amount": previous_amount,
        "current_amount": current_amount,
        "net_payable": net_payable,
    }


def _latest_previous_payment(db: Session, bill_id: uuid.UUID):
    return db.scalar(
        select(BillPreviousPayment)
        .where(BillPreviousPayment.bill_id == bill_id)
        .order_by(
            BillPreviousPayment.payment_date.desc(),
            BillPreviousPayment.id.desc(),
        )
    )


def recalculate_bill_totals(
    db: Session,
    bill_id: uuid.UUID,
) -> Bill:
    bill = db.scalar(select(Bill).where(Bill.id == bill_id))
    if not bill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bill not found",
        )

    total_items = db.scalar(
        select(func.coalesce(func.sum(BillItem.amount), 0))
        .where(BillItem.bill_id == bill_id)
    ) or Decimal("0")

    total_deductions = db.scalar(
        select(func.coalesce(func.sum(BillDeduction.amount), 0))
        .where(BillDeduction.bill_id == bill_id)
    ) or Decimal("0")

    total_tax = db.scalar(
        select(func.coalesce(func.sum(BillTax.tax_amount), 0))
        .where(BillTax.bill_id == bill_id)
    ) or Decimal("0")

    previous = _latest_previous_payment(db, bill_id)
    if previous:
        bill.previous_bill_amount = previous.previous_bill_amount
        bill.previous_payment_amount = previous.previous_payment_amount
        bill.balance_carried_forward = previous.balance_carried_forward
    else:
        bill.previous_bill_amount = Decimal("0")
        bill.previous_payment_amount = Decimal("0")
        bill.balance_carried_forward = Decimal("0")

    result = calculate_bill(
        total_items_amount=Decimal(total_items),
        other_charges=Decimal(bill.other_charges or 0),
        total_deductions=Decimal(total_deductions),
        total_tax=Decimal(total_tax),
        previous_amount=Decimal(bill.balance_carried_forward or 0),
    )

    bill.total_items_amount = result["total_items_amount"]
    bill.other_charges = result["other_charges"]
    bill.gross_amount = result["gross_amount"]
    bill.total_deductions = result["total_deductions"]
    bill.total_tax = result["total_tax"]
    bill.current_bill_amount = result["current_amount"]
    bill.net_payable_amount = result["net_payable"]
    bill.balance_amount = max(
        bill.net_payable_amount - bill.paid_amount,
        Decimal("0"),
    )

    db.add(bill)
    db.commit()
    db.refresh(bill)
    return bill


def calculate_bill_for_bill(
    db: Session,
    bill_id: uuid.UUID,
) -> BillCalculation:
    bill = recalculate_bill_totals(db, bill_id)

    calculation = BillCalculation(
        id=uuid.uuid4(),
        bill_id=bill.id,
        total_items_amount=bill.total_items_amount,
        other_charges=bill.other_charges,
        gross_amount=bill.gross_amount,
        total_deductions=bill.total_deductions,
        total_tax=bill.total_tax,
        previous_amount=bill.balance_carried_forward,
        current_amount=bill.current_bill_amount,
        net_payable=bill.net_payable_amount,
    )

    return add_bill_calculation(db, calculation)


def get_bill_calculation_for_user(
    db: Session,
    bill_id: uuid.UUID,
    user_id: uuid.UUID,
) -> BillCalculation:
    bill = db.scalar(
        select(Bill).where(
            Bill.id == bill_id,
            Bill.user_id == user_id,
        )
    )
    if not bill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bill not found",
        )

    calculation = get_bill_calculation(db, bill_id)
    if not calculation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bill calculation not found",
        )
    return calculation
