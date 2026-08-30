import uuid
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.bill import Bill
from app.models.bill_calculation import BillCalculation
from app.models.bill_deduction import BillDeduction
from app.models.bill_item import BillItem
from app.models.bill_previous_payment import BillPreviousPayment
from app.models.bill_status_history import BillStatusHistory
from app.models.bill_tax import BillTax
from app.models.bill_payment import BillPayment
from app.models.bill_type import BillType
from app.models.party import Party
from app.models.project import Project
from app.repositories.bill_repository import (
    delete_bill,
    get_bill_by_id_and_user,
    get_bill_by_number,
    get_bills,
    update_bill,
)
from app.schemas.bill import BillResponse
from app.schemas.bill_calculation import BillCalculationResponse
from app.schemas.bill_deduction import BillDeductionResponse
from app.schemas.bill_item import BillItemResponse
from app.schemas.bill_payment import BillPaymentResponse
from app.schemas.bill_previous_payment import BillPreviousPaymentResponse
from app.schemas.bill_status_history import BillStatusHistoryResponse
from app.schemas.bill_tax import BillTaxResponse

ALLOWED_STATUSES = {
    "Draft",
    "Pending",
    "Submitted",
    "Approved",
    "Partially Paid",
    "Paid",
    "Rejected",
    "Cancelled",
}

ALLOWED_TRANSITIONS = {
    "Draft": {"Submitted", "Cancelled"},
    "Submitted": {"Pending", "Approved", "Rejected"},
    "Pending": {"Approved", "Rejected"},
    "Rejected": {"Draft"},
    "Approved": {"Partially Paid", "Paid"},
    "Partially Paid": {"Paid"},
    "Paid": set(),
    "Cancelled": set(),
}


def _get_owned_bill(
    db: Session,
    bill_id: uuid.UUID,
    user_id: uuid.UUID,
) -> Bill:
    bill = get_bill_by_id_and_user(db, bill_id, user_id)
    if not bill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bill not found",
        )
    return bill


def _validate_party_and_project(
    db: Session,
    user_id: uuid.UUID,
    party_id: uuid.UUID,
    project_id: uuid.UUID,
) -> None:
    party = db.scalar(
        select(Party).where(
            Party.id == party_id,
            Party.user_id == user_id,
        )
    )
    if not party:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Selected party does not belong to the current user",
        )

    project = db.scalar(
        select(Project).where(
            Project.id == project_id,
            Project.user_id == user_id,
        )
    )
    if not project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Selected project does not belong to the current user",
        )


def _bill_response(db: Session, bill: Bill) -> BillResponse:
    items = list(
        db.scalars(
            select(BillItem)
            .where(BillItem.bill_id == bill.id)
            .order_by(BillItem.item_number)
        ).all()
    )
    deductions = list(
        db.scalars(
            select(BillDeduction)
            .where(BillDeduction.bill_id == bill.id)
            .order_by(BillDeduction.id)
        ).all()
    )
    taxes = list(
        db.scalars(
            select(BillTax)
            .where(BillTax.bill_id == bill.id)
            .order_by(BillTax.id)
        ).all()
    )
    payments = list(
        db.scalars(
            select(BillPayment)
            .where(BillPayment.bill_id == bill.id)
            .order_by(BillPayment.payment_date.desc())
        ).all()
    )
    previous_payments = list(
        db.scalars(
            select(BillPreviousPayment)
            .where(BillPreviousPayment.bill_id == bill.id)
            .order_by(BillPreviousPayment.payment_date.desc())
        ).all()
    )
    history = list(
        db.scalars(
            select(BillStatusHistory)
            .where(BillStatusHistory.bill_id == bill.id)
            .order_by(BillStatusHistory.changed_at.desc())
        ).all()
    )
    calculation = db.scalar(
        select(BillCalculation)
        .where(BillCalculation.bill_id == bill.id)
        .order_by(BillCalculation.calculated_at.desc(), BillCalculation.id.desc())
    )

    party = db.scalar(select(Party).where(Party.id == bill.party_id))
    project = db.scalar(select(Project).where(Project.id == bill.project_id))
    bill_type = db.scalar(select(BillType).where(BillType.id == bill.bill_type_id))

    data = {
        **{
            column.name: getattr(bill, column.name)
            for column in Bill.__table__.columns
        },
        "items": [BillItemResponse.model_validate(x) for x in items],
        "calculation": (
            BillCalculationResponse.model_validate(calculation)
            if calculation
            else None
        ),
        "deductions": [BillDeductionResponse.model_validate(x) for x in deductions],
        "taxes": [BillTaxResponse.model_validate(x) for x in taxes],
        "payments": [BillPaymentResponse.model_validate(x) for x in payments],
        "previous_payments": [
            BillPreviousPaymentResponse.model_validate(x)
            for x in previous_payments
        ],
        "status_history": [
            BillStatusHistoryResponse.model_validate(x) for x in history
        ],
        "party_name": party.name if party else None,
        "project_name": project.project_name if project else None,
        "bill_type_name": bill_type.name if bill_type else None,
    }
    return BillResponse.model_validate(data)


def create_new_bill(
    db: Session,
    user_id: uuid.UUID,
    bill_data,
) -> BillResponse:
    existing = get_bill_by_number(db, user_id, bill_data.bill_number)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Bill number already exists",
        )

    _validate_party_and_project(
        db,
        user_id,
        bill_data.party_id,
        bill_data.project_id,
    )

    if bill_data.work_period_from and bill_data.work_period_to:
        if bill_data.work_period_from > bill_data.work_period_to:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Work period start cannot be after work period end",
            )

    bill = Bill(
        id=uuid.uuid4(),
        user_id=user_id,
        bill_number=bill_data.bill_number,
        bill_type_id=bill_data.bill_type_id,
        party_id=bill_data.party_id,
        project_id=bill_data.project_id,
        bill_date=bill_data.bill_date,
        work_period_from=bill_data.work_period_from,
        work_period_to=bill_data.work_period_to,
        reference_number=bill_data.reference_number,
        work_order_number=bill_data.work_order_number,
        remarks=bill_data.remarks,
        currency=bill_data.currency,
        status="Draft",
        other_charges=bill_data.other_charges,
    )
    db.add(bill)
    db.flush()

    for item_data in bill_data.items:
        db.add(
            BillItem(
                id=uuid.uuid4(),
                bill_id=bill.id,
                item_number=item_data.item_number,
                description=item_data.description,
                unit_id=item_data.unit_id,
                quantity=item_data.quantity,
                rate=item_data.rate,
                amount=item_data.quantity * item_data.rate,
                remark=item_data.remark,
            )
        )

    for deduction_data in bill_data.deductions:
        db.add(
            BillDeduction(
                id=uuid.uuid4(),
                bill_id=bill.id,
                deduction_type_id=deduction_data.deduction_type_id,
                percentage=deduction_data.percentage,
                amount=deduction_data.amount,
                remarks=deduction_data.remarks,
            )
        )

    for tax_data in bill_data.taxes:
        tax_amount = (
            tax_data.taxable_amount * tax_data.percentage / Decimal("100")
        )
        db.add(
            BillTax(
                id=uuid.uuid4(),
                bill_id=bill.id,
                tax_type_id=tax_data.tax_type_id,
                percentage=tax_data.percentage,
                taxable_amount=tax_data.taxable_amount,
                tax_amount=tax_amount,
            )
        )

    if bill_data.previous_payment:
        previous = bill_data.previous_payment
        db.add(
            BillPreviousPayment(
                id=uuid.uuid4(),
                bill_id=bill.id,
                previous_bill_amount=previous.previous_bill_amount,
                previous_payment_amount=previous.previous_payment_amount,
                balance_carried_forward=previous.balance_carried_forward,
                payment_date=previous.payment_date,
                reference_number=previous.reference_number,
                remarks=previous.remarks,
            )
        )

    db.add(
        BillStatusHistory(
            id=uuid.uuid4(),
            bill_id=bill.id,
            old_status=None,
            new_status="Draft",
            changed_by=user_id,
            remarks="Bill created",
        )
    )

    db.commit()
    db.refresh(bill)

    # Calculate from actual child records rather than trusting client totals.
    from app.services.bill_calculation_service import recalculate_bill_totals
    recalculate_bill_totals(db, bill.id)
    db.refresh(bill)
    return _bill_response(db, bill)


def get_all_bills(db: Session, user_id: uuid.UUID) -> list[BillResponse]:
    bills = get_bills(db, user_id)
    if not bills:
        return []

    party_ids = {bill.party_id for bill in bills}
    project_ids = {bill.project_id for bill in bills}
    bill_type_ids = {bill.bill_type_id for bill in bills}

    parties = {
        x.id: x for x in db.scalars(select(Party).where(Party.id.in_(party_ids))).all()
    }
    projects = {
        x.id: x for x in db.scalars(select(Project).where(Project.id.in_(project_ids))).all()
    }
    bill_types = {
        x.id: x for x in db.scalars(select(BillType).where(BillType.id.in_(bill_type_ids))).all()
    }

    responses = []
    for bill in bills:
        data = {
            **{column.name: getattr(bill, column.name) for column in Bill.__table__.columns},
            "party_name": parties.get(bill.party_id).name if bill.party_id in parties else None,
            "project_name": projects.get(bill.project_id).project_name if bill.project_id in projects else None,
            "bill_type_name": bill_types.get(bill.bill_type_id).name if bill.bill_type_id in bill_types else None,
            "items": [],
            "calculation": None,
            "deductions": [],
            "taxes": [],
            "payments": [],
            "previous_payments": [],
            "status_history": [],
        }
        responses.append(BillResponse.model_validate(data))
    return responses


def get_bill(db: Session, bill_id: uuid.UUID, user_id: uuid.UUID) -> BillResponse:
    bill = _get_owned_bill(db, bill_id, user_id)
    return _bill_response(db, bill)


def update_bill_details(
    db: Session,
    bill_id: uuid.UUID,
    user_id: uuid.UUID,
    **data,
) -> BillResponse:
    bill = _get_owned_bill(db, bill_id, user_id)

    if bill.status not in {"Draft", "Rejected"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only Draft or Rejected bills can be edited",
        )

    if "bill_number" in data and data["bill_number"] != bill.bill_number:
        existing = get_bill_by_number(db, user_id, data["bill_number"])
        if existing and existing.id != bill.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Bill number already exists",
            )

    if "party_id" in data or "project_id" in data:
        _validate_party_and_project(
            db,
            user_id,
            data.get("party_id", bill.party_id),
            data.get("project_id", bill.project_id),
        )

    if data.get("work_period_from") and data.get("work_period_to"):
        if data["work_period_from"] > data["work_period_to"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Work period start cannot be after work period end",
            )

    for field, value in data.items():
        if value is not None:
            setattr(bill, field, value)

    update_bill(db, bill)
    from app.services.bill_calculation_service import recalculate_bill_totals
    recalculate_bill_totals(db, bill.id)
    db.refresh(bill)
    return _bill_response(db, bill)


def update_bill_status(
    db: Session,
    bill_id: uuid.UUID,
    user_id: uuid.UUID,
    new_status: str,
    remarks: str | None = None,
) -> BillResponse:
    bill = _get_owned_bill(db, bill_id, user_id)

    if new_status not in ALLOWED_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid bill status",
        )

    if new_status not in ALLOWED_TRANSITIONS.get(bill.status, set()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot change bill status from {bill.status} to {new_status}",
        )

    old_status = bill.status
    bill.status = new_status
    db.add(
        BillStatusHistory(
            id=uuid.uuid4(),
            bill_id=bill.id,
            old_status=old_status,
            new_status=new_status,
            changed_by=user_id,
            remarks=remarks or f"Status changed to {new_status}",
        )
    )
    db.commit()
    db.refresh(bill)
    return _bill_response(db, bill)


def delete_bill_for_user(
    db: Session,
    bill_id: uuid.UUID,
    user_id: uuid.UUID,
) -> None:
    bill = _get_owned_bill(db, bill_id, user_id)

    if bill.status not in {"Draft", "Rejected"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only Draft or Rejected bills can be deleted",
        )

    if bill.paid_amount > Decimal("0"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A bill with payments cannot be deleted",
        )

    try:
        delete_bill(db, bill)
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Bill cannot be deleted because it has dependent records that are not supported by this API",
        ) from exc
