import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Numeric, String
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import Mapped, mapped_column


from app.core.database import Base


class BillPayment(Base):
    __tablename__ = "BILL_PAYMENTS"

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

    payment_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False
    )

    payment_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    payment_mode: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    transaction_reference: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    remarks: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )