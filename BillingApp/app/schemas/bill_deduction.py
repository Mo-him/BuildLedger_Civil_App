from decimal import Decimal

from pydantic import BaseModel, Field


class BillDeductionCreate(BaseModel):
    deduction_type_id: int
    percentage: Decimal | None = Field(
        default=None,
        ge=0
    )
    amount: Decimal = Field(ge=0)
    remarks: str | None = None


class BillDeductionResponse(BillDeductionCreate):
    id: str

    model_config = {
        "from_attributes": True
    }