from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class BillCalculationCreate(BaseModel):
    total_items_amount: Decimal = Field(ge=0)
    other_charges: Decimal = Field(ge=0)
    gross_amount: Decimal = Field(ge=0)
    total_deductions: Decimal = Field(ge=0)
    total_tax: Decimal = Field(ge=0)
    previous_amount: Decimal = Field(ge=0)
    current_amount: Decimal = Field(ge=0)
    net_payable: Decimal = Field(ge=0)


class BillCalculationResponse(BillCalculationCreate):
    id: str
    calculated_at: datetime

    model_config = {"from_attributes": True}
