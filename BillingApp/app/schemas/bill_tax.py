from decimal import Decimal

from pydantic import BaseModel, Field


class BillTaxBase(BaseModel):
    tax_type_id: int
    percentage: Decimal = Field(ge=0, le=100)
    taxable_amount: Decimal = Field(ge=0)
    # Accepted for backward compatibility; backend always recalculates it.
    tax_amount: Decimal | None = Field(default=None, ge=0)


class BillTaxCreate(BillTaxBase):
    pass


class BillTaxResponse(BaseModel):
    id: str
    bill_id: str
    tax_type_id: int
    percentage: Decimal
    taxable_amount: Decimal
    tax_amount: Decimal

    model_config = {"from_attributes": True}
