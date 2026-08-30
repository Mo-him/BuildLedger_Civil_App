import uuid
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.bill import Bill
from app.models.bill_item import BillItem
from app.repositories.bill_repository import (
    add_bill_item,
    delete_bill_item,
    get_bill_item_by_id,
    get_bill_items,
    update_bill_item,
)


def _get_owned_bill(db: Session, bill_id: uuid.UUID, user_id: uuid.UUID) -> Bill:
    bill = db.scalar(
        select(Bill).where(Bill.id == bill_id, Bill.user_id == user_id)
    )
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return bill


def get_all_bill_items(db: Session, bill_id: uuid.UUID, user_id: uuid.UUID) -> list[BillItem]:
    _get_owned_bill(db, bill_id, user_id)
    return get_bill_items(db, bill_id)


def get_bill_item(
    db: Session,
    bill_id: uuid.UUID,
    item_id: uuid.UUID,
    user_id: uuid.UUID,
) -> BillItem:
    _get_owned_bill(db, bill_id, user_id)
    item = get_bill_item_by_id(db, bill_id, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Bill item not found")
    return item


def create_bill_item(
    db: Session,
    bill_id: uuid.UUID,
    user_id: uuid.UUID,
    item_number: int,
    description: str,
    unit_id: int,
    quantity: Decimal,
    rate: Decimal,
    remark: str | None = None,
) -> BillItem:
    bill = _get_owned_bill(db, bill_id, user_id)
    if bill.status not in {"Draft", "Rejected"}:
        raise HTTPException(status_code=400, detail="Items can only be changed on Draft or Rejected bills")

    item = BillItem(
        id=uuid.uuid4(),
        bill_id=bill_id,
        item_number=item_number,
        description=description,
        unit_id=unit_id,
        quantity=quantity,
        rate=rate,
        amount=quantity * rate,
        remark=remark,
    )
    saved = add_bill_item(db, item)

    from app.services.bill_calculation_service import recalculate_bill_totals
    recalculate_bill_totals(db, bill_id)
    return saved


def update_bill_item_details(
    db: Session,
    bill_id: uuid.UUID,
    item_id: uuid.UUID,
    user_id: uuid.UUID,
    **data,
) -> BillItem:
    bill = _get_owned_bill(db, bill_id, user_id)
    if bill.status not in {"Draft", "Rejected"}:
        raise HTTPException(status_code=400, detail="Items can only be changed on Draft or Rejected bills")

    item = get_bill_item_by_id(db, bill_id, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Bill item not found")

    for field in ("item_number", "description", "unit_id", "remark"):
        if field in data:
            setattr(item, field, data[field])
    if data.get("quantity") is not None:
        item.quantity = data["quantity"]
    if data.get("rate") is not None:
        item.rate = data["rate"]

    # Never trust a client-supplied amount.
    item.amount = item.quantity * item.rate
    saved = update_bill_item(db, item)

    from app.services.bill_calculation_service import recalculate_bill_totals
    recalculate_bill_totals(db, bill_id)
    return saved


def remove_bill_item(
    db: Session,
    bill_id: uuid.UUID,
    item_id: uuid.UUID,
    user_id: uuid.UUID,
) -> None:
    bill = _get_owned_bill(db, bill_id, user_id)
    if bill.status not in {"Draft", "Rejected"}:
        raise HTTPException(status_code=400, detail="Items can only be changed on Draft or Rejected bills")

    item = get_bill_item_by_id(db, bill_id, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Bill item not found")

    delete_bill_item(db, item)

    from app.services.bill_calculation_service import recalculate_bill_totals
    recalculate_bill_totals(db, bill_id)
