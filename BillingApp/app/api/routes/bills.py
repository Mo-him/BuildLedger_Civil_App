import uuid

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.schemas.bill import BillCreate, BillResponse, BillUpdate
from app.services.bill_service import (
    create_new_bill,
    delete_bill_for_user,
    get_all_bills,
    get_bill,
    update_bill_details,
    update_bill_status,
)

router = APIRouter(prefix="/bills", tags=["Bills"])


@router.get("/", response_model=list[BillResponse])
def bills(
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
):
    return get_all_bills(db=db, user_id=user_id)


@router.get("/{bill_id}", response_model=BillResponse)
def bill_by_id(
    bill_id: uuid.UUID,
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
):
    return get_bill(db=db, bill_id=bill_id, user_id=user_id)


@router.post("/", response_model=BillResponse, status_code=status.HTTP_201_CREATED)
def create(
    data: BillCreate,
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
):
    return create_new_bill(db=db, user_id=user_id, bill_data=data)


@router.put("/{bill_id}", response_model=BillResponse)
def update(
    bill_id: uuid.UUID,
    data: BillUpdate,
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
):
    return update_bill_details(
        db=db,
        bill_id=bill_id,
        user_id=user_id,
        **data.model_dump(exclude_unset=True),
    )


@router.delete("/{bill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    bill_id: uuid.UUID,
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
):
    delete_bill_for_user(db, bill_id, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{bill_id}/submit", response_model=BillResponse)
def submit_bill(
    bill_id: uuid.UUID,
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
):
    return update_bill_status(db, bill_id, user_id, "Submitted")


@router.post("/{bill_id}/approve", response_model=BillResponse)
def approve_bill(
    bill_id: uuid.UUID,
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
):
    return update_bill_status(db, bill_id, user_id, "Approved")


@router.post("/{bill_id}/reject", response_model=BillResponse)
def reject_bill(
    bill_id: uuid.UUID,
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
):
    return update_bill_status(db, bill_id, user_id, "Rejected")


@router.post("/{bill_id}/cancel", response_model=BillResponse)
def cancel_bill(
    bill_id: uuid.UUID,
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
):
    return update_bill_status(db, bill_id, user_id, "Cancelled")
