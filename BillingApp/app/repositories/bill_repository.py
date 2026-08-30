import uuid

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models.bill import Bill
from app.models.bill_calculation import BillCalculation
from app.models.bill_deduction import BillDeduction
from app.models.bill_item import BillItem
from app.models.bill_payment import BillPayment
from app.models.bill_previous_payment import BillPreviousPayment
from app.models.bill_status_history import BillStatusHistory
from app.models.bill_tax import BillTax


# =========================================================
# BILL
# =========================================================

def get_bill_by_id(db: Session, bill_id: uuid.UUID) -> Bill | None:
    return db.scalar(select(Bill).where(Bill.id == bill_id))


def get_bill_by_id_and_user(
    db: Session,
    bill_id: uuid.UUID,
    user_id: uuid.UUID,
) -> Bill | None:
    return db.scalar(
        select(Bill).where(
            Bill.id == bill_id,
            Bill.user_id == user_id,
        )
    )


def get_bills(db: Session, user_id: uuid.UUID) -> list[Bill]:
    return list(
        db.scalars(
            select(Bill)
            .where(Bill.user_id == user_id)
            .order_by(Bill.bill_date.desc(), Bill.bill_number.desc())
        ).all()
    )


def get_bill_by_number(
    db: Session,
    user_id: uuid.UUID,
    bill_number: str,
) -> Bill | None:
    return db.scalar(
        select(Bill).where(
            Bill.user_id == user_id,
            Bill.bill_number == bill_number,
        )
    )


def create_bill(db: Session, bill: Bill) -> Bill:
    db.add(bill)
    db.commit()
    db.refresh(bill)
    return bill


def update_bill(db: Session, bill: Bill) -> Bill:
    db.commit()
    db.refresh(bill)
    return bill


def delete_bill(db: Session, bill: Bill) -> None:
    # Delete known bill children first because the existing SQL schema
    # does not rely on ON DELETE CASCADE for these tables.
    child_tables = (
        BillStatusHistory,
        BillPayment,
        BillPreviousPayment,
        BillTax,
        BillDeduction,
        BillCalculation,
        BillItem,
    )
    for model in child_tables:
        db.execute(delete(model).where(model.bill_id == bill.id))

    db.delete(bill)
    db.commit()


# =========================================================
# BILL ITEMS
# =========================================================

def get_bill_items(db: Session, bill_id: uuid.UUID) -> list[BillItem]:
    return list(
        db.scalars(
            select(BillItem)
            .where(BillItem.bill_id == bill_id)
            .order_by(BillItem.item_number)
        ).all()
    )


def get_bill_item_by_id(
    db: Session,
    bill_id: uuid.UUID,
    item_id: uuid.UUID,
) -> BillItem | None:
    return db.scalar(
        select(BillItem).where(
            BillItem.id == item_id,
            BillItem.bill_id == bill_id,
        )
    )


def add_bill_item(db: Session, item: BillItem) -> BillItem:
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_bill_item(db: Session, item: BillItem) -> BillItem:
    db.commit()
    db.refresh(item)
    return item


def delete_bill_item(db: Session, item: BillItem) -> None:
    db.delete(item)
    db.commit()


# =========================================================
# BILL CALCULATION
# =========================================================

def get_bill_calculation(
    db: Session,
    bill_id: uuid.UUID,
) -> BillCalculation | None:
    return db.scalar(
        select(BillCalculation)
        .where(BillCalculation.bill_id == bill_id)
        .order_by(BillCalculation.calculated_at.desc(), BillCalculation.id.desc())
    )


def add_bill_calculation(
    db: Session,
    calculation: BillCalculation,
) -> BillCalculation:
    db.add(calculation)
    db.commit()
    db.refresh(calculation)
    return calculation


# =========================================================
# BILL DEDUCTIONS
# =========================================================

def get_bill_deductions(db: Session, bill_id: uuid.UUID) -> list[BillDeduction]:
    return list(
        db.scalars(
            select(BillDeduction)
            .where(BillDeduction.bill_id == bill_id)
            .order_by(BillDeduction.id)
        ).all()
    )


def get_bill_deduction_by_id(
    db: Session,
    bill_id: uuid.UUID,
    deduction_id: uuid.UUID,
) -> BillDeduction | None:
    return db.scalar(
        select(BillDeduction).where(
            BillDeduction.id == deduction_id,
            BillDeduction.bill_id == bill_id,
        )
    )


def add_bill_deduction(db: Session, deduction: BillDeduction) -> BillDeduction:
    db.add(deduction)
    db.commit()
    db.refresh(deduction)
    return deduction


def update_bill_deduction(db: Session, deduction: BillDeduction) -> BillDeduction:
    db.commit()
    db.refresh(deduction)
    return deduction


def delete_bill_deduction(db: Session, deduction: BillDeduction) -> None:
    db.delete(deduction)
    db.commit()


# =========================================================
# BILL TAXES
# =========================================================

def get_bill_taxes(db: Session, bill_id: uuid.UUID) -> list[BillTax]:
    return list(
        db.scalars(
            select(BillTax)
            .where(BillTax.bill_id == bill_id)
            .order_by(BillTax.id)
        ).all()
    )


def get_bill_tax_by_id(
    db: Session,
    bill_id: uuid.UUID,
    tax_id: uuid.UUID,
) -> BillTax | None:
    return db.scalar(
        select(BillTax).where(
            BillTax.id == tax_id,
            BillTax.bill_id == bill_id,
        )
    )


def add_bill_tax(db: Session, tax: BillTax) -> BillTax:
    db.add(tax)
    db.commit()
    db.refresh(tax)
    return tax


def update_bill_tax(db: Session, tax: BillTax) -> BillTax:
    db.commit()
    db.refresh(tax)
    return tax


def delete_bill_tax(db: Session, tax: BillTax) -> None:
    db.delete(tax)
    db.commit()


# =========================================================
# BILL PAYMENTS
# =========================================================

def get_bill_payments(db: Session, bill_id: uuid.UUID) -> list[BillPayment]:
    return list(
        db.scalars(
            select(BillPayment)
            .where(BillPayment.bill_id == bill_id)
            .order_by(BillPayment.payment_date.desc())
        ).all()
    )


def get_bill_payment_by_id(
    db: Session,
    bill_id: uuid.UUID,
    payment_id: uuid.UUID,
) -> BillPayment | None:
    return db.scalar(
        select(BillPayment).where(
            BillPayment.id == payment_id,
            BillPayment.bill_id == bill_id,
        )
    )


def add_bill_payment(db: Session, payment: BillPayment) -> BillPayment:
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


def update_bill_payment(db: Session, payment: BillPayment) -> BillPayment:
    db.commit()
    db.refresh(payment)
    return payment


def delete_bill_payment(db: Session, payment: BillPayment) -> None:
    db.delete(payment)
    db.commit()


# =========================================================
# PREVIOUS PAYMENTS
# =========================================================

def get_previous_payments(
    db: Session,
    bill_id: uuid.UUID,
) -> list[BillPreviousPayment]:
    return list(
        db.scalars(
            select(BillPreviousPayment)
            .where(BillPreviousPayment.bill_id == bill_id)
            .order_by(BillPreviousPayment.payment_date.desc())
        ).all()
    )


def get_previous_payment_by_id(
    db: Session,
    bill_id: uuid.UUID,
    previous_payment_id: uuid.UUID,
) -> BillPreviousPayment | None:
    return db.scalar(
        select(BillPreviousPayment).where(
            BillPreviousPayment.id == previous_payment_id,
            BillPreviousPayment.bill_id == bill_id,
        )
    )


def add_previous_payment(
    db: Session,
    payment: BillPreviousPayment,
) -> BillPreviousPayment:
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


def update_previous_payment(
    db: Session,
    payment: BillPreviousPayment,
) -> BillPreviousPayment:
    db.commit()
    db.refresh(payment)
    return payment


def delete_previous_payment(
    db: Session,
    payment: BillPreviousPayment,
) -> None:
    db.delete(payment)
    db.commit()


# =========================================================
# BILL STATUS HISTORY
# =========================================================

def get_status_history(
    db: Session,
    bill_id: uuid.UUID,
) -> list[BillStatusHistory]:
    return list(
        db.scalars(
            select(BillStatusHistory)
            .where(BillStatusHistory.bill_id == bill_id)
            .order_by(BillStatusHistory.changed_at.desc())
        ).all()
    )


def add_status_history(
    db: Session,
    history: BillStatusHistory,
) -> BillStatusHistory:
    db.add(history)
    db.commit()
    db.refresh(history)
    return history
