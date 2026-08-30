from datetime import datetime

from pydantic import BaseModel


class BillStatusHistoryCreate(BaseModel):
    old_status: str | None = None
    new_status: str
    changed_by: str
    remarks: str | None = None


class BillStatusHistoryResponse(BaseModel):
    id: str
    bill_id: str
    old_status: str | None = None
    new_status: str
    changed_by: str
    remarks: str | None = None
    changed_at: datetime

    model_config = {"from_attributes": True}
