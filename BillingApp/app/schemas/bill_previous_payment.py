from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


class BillPreviousPaymentCreate(BaseModel):
    previous_bill_amount: Decimal = Field(ge=0)
    previous_payment_amount: Decimal = Field(ge=0)
    balance_carried_forward: Decimal = Field(ge=0)
    payment_date: date
    reference_number: str | None = None
    remarks: str | None = None


class BillPreviousPaymentUpdate(BaseModel):
    previous_bill_amount: Decimal | None = Field(default=None, ge=0)
    previous_payment_amount: Decimal | None = Field(default=None, ge=0)
    balance_carried_forward: Decimal | None = Field(default=None, ge=0)
    payment_date: date | None = None
    reference_number: str | None = None
    remarks: str | None = None


class BillPreviousPaymentResponse(BillPreviousPaymentCreate):
    id: str
    bill_id: str

    model_config = {"from_attributes": True}
