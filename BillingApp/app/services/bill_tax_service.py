import uuid
from decimal import Decimal, ROUND_HALF_UP

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.bill import Bill
from app.models.bill_tax import BillTax
from app.repositories.bill_repository import (
    add_bill_tax,
    delete_bill_tax,
    get_bill_tax_by_id,
    get_bill_taxes,
    update_bill_tax,
)


def _get_owned_bill(db: Session, bill_id: uuid.UUID, user_id: uuid.UUID) -> Bill:
    bill = db.scalar(select(Bill).where(Bill.id == bill_id, Bill.user_id == user_id))
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return bill


def get_all_bill_taxes(db: Session, bill_id: uuid.UUID, user_id: uuid.UUID) -> list[BillTax]:
    _get_owned_bill(db, bill_id, user_id)
    return get_bill_taxes(db, bill_id)


def get_bill_tax(db: Session, bill_id: uuid.UUID, tax_id: uuid.UUID, user_id: uuid.UUID) -> BillTax:
    _get_owned_bill(db, bill_id, user_id)
    tax = get_bill_tax_by_id(db, bill_id, tax_id)
    if not tax:
        raise HTTPException(status_code=404, detail="Bill tax not found")
    return tax


def _tax_amount(taxable_amount: Decimal, percentage: Decimal) -> Decimal:
    return (taxable_amount * percentage / Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def create_bill_tax(db: Session, bill_id: uuid.UUID, user_id: uuid.UUID, tax_type_id: int, percentage: Decimal, taxable_amount: Decimal, tax_amount: Decimal | None = None) -> BillTax:
    bill = _get_owned_bill(db, bill_id, user_id)
    if bill.status not in {"Draft", "Rejected"}:
        raise HTTPException(status_code=400, detail="Taxes can only be changed on Draft or Rejected bills")
    if not 0 <= percentage <= 100 or taxable_amount < 0:
        raise HTTPException(status_code=400, detail="Invalid tax percentage or taxable amount")

    calculated = _tax_amount(taxable_amount, percentage)
    tax = BillTax(
        id=uuid.uuid4(), bill_id=bill_id, tax_type_id=tax_type_id,
        percentage=percentage, taxable_amount=taxable_amount, tax_amount=calculated,
    )
    saved = add_bill_tax(db, tax)
    from app.services.bill_calculation_service import recalculate_bill_totals
    recalculate_bill_totals(db, bill_id)
    return saved


def update_bill_tax_details(db: Session, bill_id: uuid.UUID, tax_id: uuid.UUID, user_id: uuid.UUID, **data) -> BillTax:
    bill = _get_owned_bill(db, bill_id, user_id)
    if bill.status not in {"Draft", "Rejected"}:
        raise HTTPException(status_code=400, detail="Taxes can only be changed on Draft or Rejected bills")
    tax = get_bill_tax(db, bill_id, tax_id, user_id)
    if data.get("percentage") is not None and not 0 <= data["percentage"] <= 100:
        raise HTTPException(status_code=400, detail="Tax percentage must be between 0 and 100")
    if data.get("taxable_amount") is not None and data["taxable_amount"] < 0:
        raise HTTPException(status_code=400, detail="Taxable amount cannot be negative")

    for field, value in data.items():
        if value is not None and field != "tax_amount":
            setattr(tax, field, value)
    tax.tax_amount = _tax_amount(tax.taxable_amount, tax.percentage)
    saved = update_bill_tax(db, tax)
    from app.services.bill_calculation_service import recalculate_bill_totals
    recalculate_bill_totals(db, bill_id)
    return saved


def remove_bill_tax(db: Session, bill_id: uuid.UUID, tax_id: uuid.UUID, user_id: uuid.UUID) -> None:
    bill = _get_owned_bill(db, bill_id, user_id)
    if bill.status not in {"Draft", "Rejected"}:
        raise HTTPException(status_code=400, detail="Taxes can only be changed on Draft or Rejected bills")
    tax = get_bill_tax(db, bill_id, tax_id, user_id)
    delete_bill_tax(db, tax)
    from app.services.bill_calculation_service import recalculate_bill_totals
    recalculate_bill_totals(db, bill_id)
