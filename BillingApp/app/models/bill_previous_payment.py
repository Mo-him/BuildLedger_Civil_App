import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Numeric, String
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class BillPreviousPayment(Base):
    __tablename__ = "BILL_PREVIOUS_PAYMENTS"

    id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4
    )
    bill_id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER, ForeignKey("BILLS.id"), nullable=False
    )
    previous_bill_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), nullable=False
    )
    previous_payment_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), nullable=False
    )
    balance_carried_forward: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), nullable=False
    )
    payment_date: Mapped[date] = mapped_column(Date, nullable=False)
    reference_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    remarks: Mapped[str | None] = mapped_column(String(255), nullable=True)
