from decimal import Decimal

from pydantic import BaseModel, Field


class BillItemCreate(BaseModel):
    item_number: int = Field(ge=1)
    description: str
    unit_id: int
    quantity: Decimal = Field(ge=0)
    rate: Decimal = Field(ge=0)
    # Accepted for backward compatibility, but the API always recalculates it.
    amount: Decimal | None = Field(default=None, ge=0)
    remark: str | None = None


class BillItemUpdate(BaseModel):
    item_number: int | None = Field(default=None, ge=1)
    description: str | None = None
    unit_id: int | None = None
    quantity: Decimal | None = Field(default=None, ge=0)
    rate: Decimal | None = Field(default=None, ge=0)
    amount: Decimal | None = Field(default=None, ge=0)
    remark: str | None = None


class BillItemResponse(BaseModel):
    id: str
    item_number: int
    description: str
    unit_id: int
    quantity: Decimal
    rate: Decimal
    amount: Decimal
    remark: str | None = None

    model_config = {"from_attributes": True}
