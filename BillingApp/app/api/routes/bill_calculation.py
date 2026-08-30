import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.schemas.bill_calculation import BillCalculationResponse
from app.services.bill_calculation_service import (
    calculate_bill_for_bill,
    get_bill_calculation_for_user,
)

router = APIRouter(prefix="/bills/{bill_id}/calculation", tags=["Bill Calculation"])


@router.post("", response_model=BillCalculationResponse)
def calculate(
    bill_id: uuid.UUID,
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
):
    from app.services.bill_service import get_bill
    get_bill(db, bill_id, user_id)
    return calculate_bill_for_bill(db, bill_id)


@router.get("", response_model=BillCalculationResponse)
def get_calculation(
    bill_id: uuid.UUID,
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
):
    return get_bill_calculation_for_user(db, bill_id, user_id)
