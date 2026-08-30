import uuid
from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field

from app.schemas.bill_calculation import BillCalculationCreate, BillCalculationResponse
from app.schemas.bill_deduction import BillDeductionCreate, BillDeductionResponse
from app.schemas.bill_item import BillItemCreate, BillItemResponse
from app.schemas.bill_payment import BillPaymentResponse
from app.schemas.bill_previous_payment import (
    BillPreviousPaymentCreate,
    BillPreviousPaymentResponse,
)
from app.schemas.bill_status_history import BillStatusHistoryResponse
from app.schemas.bill_tax import BillTaxCreate, BillTaxResponse


class BillBase(BaseModel):
    bill_number: str
    bill_type_id: int
    party_id: uuid.UUID
    project_id: uuid.UUID
    bill_date: date
    work_period_from: date | None = None
    work_period_to: date | None = None
    reference_number: str | None = None
    work_order_number: str | None = None
    remarks: str | None = None
    currency: str = "INR"
    status: str = "Draft"

    total_items_amount: Decimal = Field(default=0, ge=0)
    other_charges: Decimal = Field(default=0, ge=0)
    gross_amount: Decimal = Field(default=0, ge=0)
    total_deductions: Decimal = Field(default=0, ge=0)
    total_tax: Decimal = Field(default=0, ge=0)
    previous_bill_amount: Decimal = Field(default=0, ge=0)
    previous_payment_amount: Decimal = Field(default=0, ge=0)
    balance_carried_forward: Decimal = Field(default=0, ge=0)
    current_bill_amount: Decimal = Field(default=0, ge=0)
    net_payable_amount: Decimal = Field(default=0, ge=0)
    paid_amount: Decimal = Field(default=0, ge=0)
    balance_amount: Decimal = Field(default=0, ge=0)


class BillCreate(BaseModel):
    bill_number: str
    bill_type_id: int
    party_id: uuid.UUID
    project_id: uuid.UUID
    bill_date: date
    work_period_from: date | None = None
    work_period_to: date | None = None
    reference_number: str | None = None
    work_order_number: str | None = None
    remarks: str | None = None
    currency: str = "INR"
    other_charges: Decimal = Field(default=0, ge=0)

    items: list[BillItemCreate] = Field(default_factory=list)
    calculation: BillCalculationCreate | None = None
    deductions: list[BillDeductionCreate] = Field(default_factory=list)
    taxes: list[BillTaxCreate] = Field(default_factory=list)
    previous_payment: BillPreviousPaymentCreate | None = None


class BillUpdate(BaseModel):
    bill_number: str | None = None
    bill_type_id: int | None = None
    party_id: uuid.UUID | None = None
    project_id: uuid.UUID | None = None
    bill_date: date | None = None
    work_period_from: date | None = None
    work_period_to: date | None = None
    reference_number: str | None = None
    work_order_number: str | None = None
    remarks: str | None = None
    currency: str | None = None
    other_charges: Decimal | None = Field(default=None, ge=0)


class BillResponse(BillBase):
    id: uuid.UUID
    user_id: uuid.UUID
    party_name: str | None = None
    project_name: str | None = None
    bill_type_name: str | None = None
    items: list[BillItemResponse] = Field(default_factory=list)
    calculation: BillCalculationResponse | None = None
    deductions: list[BillDeductionResponse] = Field(default_factory=list)
    taxes: list[BillTaxResponse] = Field(default_factory=list)
    payments: list[BillPaymentResponse] = Field(default_factory=list)
    previous_payments: list[BillPreviousPaymentResponse] = Field(default_factory=list)
    status_history: list[BillStatusHistoryResponse] = Field(default_factory=list)

    model_config = {"from_attributes": True}
