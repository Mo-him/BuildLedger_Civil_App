import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, text
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class BillStatusHistory(Base):
    __tablename__ = "BILL_STATUS_HISTORY"

    id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4
    )
    bill_id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER, ForeignKey("BILLS.id"), nullable=False
    )
    old_status: Mapped[str | None] = mapped_column(String(30), nullable=True)
    new_status: Mapped[str] = mapped_column(String(30), nullable=False)
    changed_by: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER, ForeignKey("USERS.id"), nullable=False
    )
    remarks: Mapped[str | None] = mapped_column(String(255), nullable=True)
    changed_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("GETDATE()"),
    )
