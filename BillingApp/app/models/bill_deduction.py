import uuid
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class BillDeduction(Base):
    __tablename__ = "BILL_DEDUCTIONS"

    id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER,
        primary_key=True,
        default=uuid.uuid4
    )

    bill_id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER,
        ForeignKey("BILLS.id"),
        nullable=False
    )

    deduction_type_id: Mapped[int] = mapped_column(
        ForeignKey("DEDUCTION_TYPES.id"),
        nullable=False
    )

    percentage: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2),
        nullable=True
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False
    )

    remarks: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )