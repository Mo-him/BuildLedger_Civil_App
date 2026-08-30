from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.party_type import PartyType
from app.models.bill_type import BillType
from app.models.unit import Unit
from app.models.deduction_type import DeductionType
from app.models.tax_type import TaxType


class MasterRepository:

    @staticmethod
    def get_party_types(db: Session):
        statement = (
            select(PartyType)
            .where(PartyType.is_active == True)
            .order_by(PartyType.name)
        )

        return db.scalars(statement).all()

    @staticmethod
    def get_bill_types(db: Session):
        statement = (
            select(BillType)
            .where(BillType.is_active == True)
            .order_by(BillType.name)
        )

        return db.scalars(statement).all()

    @staticmethod
    def get_units(db: Session):
        statement = (
            select(Unit)
            .where(Unit.is_active == True)
            .order_by(Unit.unit_name)
        )

        return db.scalars(statement).all()

    @staticmethod
    def get_deduction_types(db: Session):
        statement = (
            select(DeductionType)
            .where(DeductionType.is_active == True)
            .order_by(DeductionType.name)
        )

        return db.scalars(statement).all()

    @staticmethod
    def get_tax_types(db: Session):
        statement = (
            select(TaxType)
            .where(TaxType.is_active == True)
            .order_by(TaxType.name)
        )

        return db.scalars(statement).all()


master_repository = MasterRepository()