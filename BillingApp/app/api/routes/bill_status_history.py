import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.schemas.bill_status_history import BillStatusHistoryResponse
from app.services.bill_status_history_service import get_bill_status_history

router = APIRouter(prefix="/bills/{bill_id}/status-history", tags=["Bill Status History"])


@router.get("", response_model=list[BillStatusHistoryResponse])
def get_status_history(
    bill_id: uuid.UUID,
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
):
    return get_bill_status_history(db, bill_id, user_id)
