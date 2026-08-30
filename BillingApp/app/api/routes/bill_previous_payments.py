import uuid

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.schemas.bill_previous_payment import (
    BillPreviousPaymentCreate,
    BillPreviousPaymentResponse,
    BillPreviousPaymentUpdate,
)
from app.services.bill_previous_payment_service import (
    create_previous_payment,
    get_all_previous_payments,
    get_previous_payment,
    remove_previous_payment,
    update_previous_payment_details,
)

router = APIRouter(prefix="/bills/{bill_id}/previous-payments", tags=["Previous Payments"])


@router.get("", response_model=list[BillPreviousPaymentResponse])
def get_previous_payments(bill_id: uuid.UUID, db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_current_user_id)):
    return get_all_previous_payments(db, bill_id, user_id)


@router.post("", response_model=BillPreviousPaymentResponse, status_code=status.HTTP_201_CREATED)
def create_previous_payment_entry(bill_id: uuid.UUID, payment: BillPreviousPaymentCreate, db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_current_user_id)):
    return create_previous_payment(db=db, bill_id=bill_id, user_id=user_id, **payment.model_dump())


@router.get("/{payment_id}", response_model=BillPreviousPaymentResponse)
def get_previous_payment_entry(bill_id: uuid.UUID, payment_id: uuid.UUID, db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_current_user_id)):
    return get_previous_payment(db, bill_id, payment_id, user_id)


@router.put("/{payment_id}", response_model=BillPreviousPaymentResponse)
def update_previous_payment_entry(bill_id: uuid.UUID, payment_id: uuid.UUID, payment: BillPreviousPaymentUpdate, db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_current_user_id)):
    return update_previous_payment_details(db=db, bill_id=bill_id, previous_payment_id=payment_id, user_id=user_id, **payment.model_dump(exclude_unset=True))


@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_previous_payment_entry(bill_id: uuid.UUID, payment_id: uuid.UUID, db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_current_user_id)):
    remove_previous_payment(db, bill_id, payment_id, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
