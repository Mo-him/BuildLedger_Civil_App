import uuid

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.models.bill import Bill

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary")
def dashboard_summary(
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
):
    base = select(Bill).where(Bill.user_id == user_id)

    def count_status(status_value: str) -> int:
        return db.scalar(
            select(func.count(Bill.id)).where(
                Bill.user_id == user_id,
                Bill.status == status_value,
            )
        ) or 0

    total_bills = db.scalar(select(func.count(Bill.id)).where(Bill.user_id == user_id)) or 0
    total_bill_amount = db.scalar(
        select(func.coalesce(func.sum(Bill.net_payable_amount), 0)).where(Bill.user_id == user_id)
    ) or 0
    total_paid = db.scalar(
        select(func.coalesce(func.sum(Bill.paid_amount), 0)).where(Bill.user_id == user_id)
    ) or 0
    total_balance = db.scalar(
        select(func.coalesce(func.sum(Bill.balance_amount), 0)).where(Bill.user_id == user_id)
    ) or 0

    recent = db.scalars(
        base.order_by(Bill.bill_date.desc(), Bill.bill_number.desc()).limit(5)
    ).all()

    return {
        "total_bills": total_bills,
        "total_bill_amount": total_bill_amount,
        "draft_count": count_status("Draft"),
        "pending_count": count_status("Pending"),
        "submitted_count": count_status("Submitted"),
        "approved_count": count_status("Approved"),
        "partially_paid_count": count_status("Partially Paid"),
        "paid_count": count_status("Paid"),
        "rejected_count": count_status("Rejected"),
        "cancelled_count": count_status("Cancelled"),
        "total_paid": total_paid,
        "total_balance": total_balance,
        "recent_bills": [
            {
                "id": bill.id,
                "bill_number": bill.bill_number,
                "bill_type_id": bill.bill_type_id,
                "party_id": bill.party_id,
                "project_id": bill.project_id,
                "bill_date": bill.bill_date,
                "status": bill.status,
                "net_payable_amount": bill.net_payable_amount,
                "paid_amount": bill.paid_amount,
                "balance_amount": bill.balance_amount,
            }
            for bill in recent
        ],
    }
