import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, text
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class BillCalculation(Base):
    __tablename__ = "BILL_CALCULATIONS"

    id: Mapped[uuid.UUID] = mapped_column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    bill_id: Mapped[uuid.UUID] = mapped_column(UNIQUEIDENTIFIER, ForeignKey("BILLS.id"), nullable=False)
    total_items_amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    other_charges: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    gross_amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    total_deductions: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    total_tax: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    previous_amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    current_amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    net_payable: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    calculated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("GETDATE()")
    )
