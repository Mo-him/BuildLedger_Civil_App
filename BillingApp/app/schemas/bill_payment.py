from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


class BillPaymentCreate(BaseModel):
    payment_amount: Decimal = Field(gt=0)
    payment_date: date
    payment_mode: str
    transaction_reference: str | None = None
    remarks: str | None = None


class BillPaymentUpdate(BaseModel):
    payment_amount: Decimal | None = Field(default=None, gt=0)
    payment_date: date | None = None
    payment_mode: str | None = None
    transaction_reference: str | None = None
    remarks: str | None = None


class BillPaymentResponse(BillPaymentCreate):
    id: str
    bill_id: str

    model_config = {"from_attributes": True}
