import uuid

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class UserSettings(Base):
    __tablename__ = "USER_SETTINGS"

    user_id: Mapped[uuid.UUID] = mapped_column(
         UNIQUEIDENTIFIER,
         ForeignKey("USERS.id"),
         primary_key=True
    )

    theme: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="light"
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default="INR"
    )

    date_format: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="DD-MM-YYYY"
    )

    notifications_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    auto_save: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )