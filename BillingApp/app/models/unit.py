from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Unit(Base):
    __tablename__ = "UNITS"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    unit_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    unit_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )